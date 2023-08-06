#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2017 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals


import io
import os
import unittest


from byov import (
    config,
    errors,
)


from byoci.slave import containers
from byoci.tests.slave import fixtures


class TestContainerErrors(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        self.out = io.StringIO()
        self.err = io.StringIO()

    def test_setup_unknown(self):
        c = containers.Container('i-dont-exist', out=self.out, err=self.err)
        with self.assertRaises(containers.errors.CommandError) as cm:
            c.setup()
        self.assertEqual(255, cm.exception.retcode)
        err = self.err.getvalue()
        self.assertTrue('i-dont-exist' in err, err)


class TestContainer(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        fixtures.define_uniq_container(self)
        self.out = io.StringIO()
        self.err = io.StringIO()

    def Container(self):
        c = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.assertEqual('UNKNOWN', c.status())
        return c

    def test_setup(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        self.assertEqual('RUNNING', c.status())

    def test_teardown(self):
        c = self.Container()
        try:
            c.setup()
        except errors.CommandError:
            # if setup() fails here, the test pre-requisites are violated. This
            # happens in RL at least when lxd fails to provide an IP and in
            # this specific case, leak the container.
            self.addCleanup(c.teardown)  # Catch up
            # re-raise as the test fails
            # FIXME: Arguably that could be a skip as the test infra is failing
            # here rather than the test itself -- vila 2018-02-23
            raise
        self.assertEqual('RUNNING', c.status())
        c.teardown()
        # The container has been stopped as part of the teardown
        self.assertEqual('UNKNOWN', c.status())

    def test_shell_success(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        user = c.shell(['whoami'])[1]
        self.assertEqual('ubuntu\n', user)

    def test_shell_error(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        with self.assertRaises(errors.CommandError) as cm:
            c.shell(['i-dont-exist'])
        # 255 (instead of 127) says ssh sees an error... maybe some pipe is not
        # closed properly ?  This smells like a FIXME...
        self.assertEqual(255, cm.exception.retcode)
        self.assertTrue('retcode: 127\n' in cm.exception.err, cm.exception.err)
        self.assertTrue('i-dont-exist: command not found' in cm.exception.err,
                        cm.exception.err)

    def test_setup_ssh(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        known_hosts = c.shell(['ls', '~/.ssh/known_hosts'])[1]
        self.assertEqual('/home/ubuntu/.ssh/known_hosts\n', known_hosts)


class TestContainerSecrets(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        fixtures.define_uniq_container(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.container = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.addCleanup(self.container.teardown)
        self.container.setup()
        # Starts with an empty secrets directory (in real life, this is where
        # the secrets branch is installed so it always exists.
        # FIXME: Shouldn't that be {{byoci}.secrets} ? -- vila 2018-02-23
        self.secrets_dir = os.path.expanduser('~/secrets')
        os.mkdir(self.secrets_dir)

    def set_secrets(self, secrets):
        conf = config.VmStack(self.container_name)
        conf.set('project.secrets', secrets)
        conf.store.save()

    def test_no_secrets(self):
        # Just a smoke test
        self.container.inject_secrets()

    def test_one_secret(self):
        secret = 'burn before reading \n'
        local_path = os.path.join(self.secrets_dir, 'secret')
        with open(local_path, 'w') as f:
            f.write(secret)
        # A path that doesn't exist in the container to test directory creation
        container_path = '.config/secrets/secret'
        self.set_secrets(local_path + ':' + container_path)
        self.container.inject_secrets()
        secret_in_container = self.container.shell(['cat', container_path])[1]
        self.assertEqual(secret, secret_in_container)

    def test_broken_secret(self):
        self.set_secrets('broken')
        with self.assertRaises(ValueError) as cm:
            self.container.inject_secrets()
        self.assertEqual('not enough values to unpack (expected 2, got 1)',
                         cm.exception.args[0])

    def test_unknown_source_secret(self):
        self.set_secrets('i-dont-exist:whatever')
        with self.assertRaises(containers.errors.CommandError) as cm:
            self.container.inject_secrets()
        # Error provides enough context
        self.assertTrue('i-dont-exist: no such file or directory' in
                        cm.exception.err)


class TestWorkerErrors(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)

    def test_start_unknown_backing(self):
        w = containers.Worker('boo', 'i-dont-exist')
        with self.assertRaises(errors.CommandError) as cm:
            w.start()
        self.assertEqual(255, cm.exception.retcode)
        self.assertTrue('i-dont-exist' in cm.exception.err)


class TestWorker(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        fixtures.define_uniq_container(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        # Spy the Container.setup calls
        self.setup_calls = 0
        orig_setup = containers.Container.setup

        def wrapped_setup(*args, **kwargs):
            self.setup_calls += 1
            return orig_setup(*args, **kwargs)

        fixtures.patch(self, containers.Container, 'setup', wrapped_setup)

    def Container(self):
        c = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.assertEqual('UNKNOWN', c.status())
        return c

    def Worker(self):
        w = containers.Worker('worker-{}'.format(self.container_name),
                              self.container_name, out=self.out, err=self.err)
        return w

    def test_backing_not_setup(self):
        c = self.Container()
        w = self.Worker()
        self.addCleanup(w.stop)
        self.addCleanup(c.teardown)
        w.start()
        self.assertEqual('RUNNING', w.status())
        # container is setup once
        self.assertEqual(1, self.setup_calls)

    def test_backing_fails_setup(self):
        c = self.Container()
        # Sabotage the base container
        conf = config.VmStack(self.container_name)
        conf.set('vm.packages', 'i-dont-exist')
        conf.store.save()
        conf.store.unload()
        w = self.Worker()
        with self.assertRaises(containers.errors.CommandError) as cm:
            w.start()
        self.assertEqual(255, cm.exception.retcode)
        errors = self.err.getvalue()
        self.assertTrue('Unable to locate package i-dont-exist\n'
                        in errors, errors)
        self.assertEqual('UNKNOWN', c.status())
        # container is setup once
        self.assertEqual(1, self.setup_calls)

    def test_backing_requires_update(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        c.stop()
        self.assertEqual('STOPPED', c.status())
        first_digest = c.digest()
        # container has been setup
        self.assertEqual(1, self.setup_calls)
        # Add a package known to be already installed just to trigger a digest
        # change
        c.config(['vm.packages=cloud-init'])
        new_digest = c.digest()
        self.assertNotEqual(first_digest, new_digest)
        w = self.Worker()
        self.addCleanup(w.stop)
        w.start()
        self.assertEqual('RUNNING', w.status())
        self.assertEqual(new_digest, c.digest())
        # container was setup again
        self.assertEqual(2, self.setup_calls)

    def test_backing_up_to_date(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        c.stop()
        self.assertEqual('STOPPED', c.status())
        # container has been setup
        self.assertEqual(1, self.setup_calls)
        w = self.Worker()
        self.addCleanup(w.stop)
        w.start()
        self.assertEqual('RUNNING', w.status())
        # container wasn't setup again
        self.assertEqual(1, self.setup_calls)

    def test_mounts_shorter_paths(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        c.stop()
        self.assertEqual('STOPPED', c.status())
        w = self.Worker()
        self.addCleanup(w.stop)
        os.mkdir('workspace')
        os.mkdir('workspace/subdir')
        os.mkdir('workspace/subdir/job')
        w.start(['workspace:/home/ubuntu/ws',
                 'workspace/subdir/job:/home/ubuntu/ws/job'])
        ret, out, err = w.shell(['touch', 'ws/job/inside'])
        self.assertEqual(0, ret)
        self.assertEqual('', out)
        # The file is seen from the host
        self.assertTrue(os.path.exists('workspace/subdir/job/inside'))
        # container wasn't setup again
        self.assertEqual(1, self.setup_calls)

    def test_mounts_longer_paths(self):
        c = self.Container()
        self.addCleanup(c.teardown)
        c.setup()
        c.stop()
        self.assertEqual('STOPPED', c.status())
        w = self.Worker()
        self.addCleanup(w.stop)
        os.mkdir('workspace')
        os.mkdir('workspace/job')
        # Trying to shorten the path my mounting a sub-sub directory inside an
        # already mounted directory is a bad idea: it leaves files owned by
        # root inside the container that cannot be deleted by a regular user on
        # the host.
        w.start(['workspace:/home/ubuntu/ws',
                 'workspace/job:/home/ubuntu/ws/subdir/job'])
        # FIXME: This pass, but with subdir being owned by root: i.e. missing
        # directories are created by lxd. This may work for some jobs but may
        # break for others -- vila 2017-01-24
        # FIXME: This also leak on the host with files that can't be deleted ?
        # -- vila 2018-01-12
        ret, out, err = w.shell(['touch', 'ws/subdir/job/inside'])
        self.assertEqual(0, ret)
        self.assertEqual('', out)
        # The file is seen from the host
        self.assertTrue(os.path.exists('workspace/job/inside'))
        # container wasn't setup again
        self.assertEqual(1, self.setup_calls)
        # Avoid leaks on files owned by root inside the vm that cannot be
        # deleted by shutil.rmtree during the regular cleanup
        ret, out, err = w.shell(['sudo', 'umount', 'ws/subdir/job',
                                 '&&', 'sudo rm -fr ws/subdir'])
