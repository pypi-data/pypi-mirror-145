# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
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

import io
import unittest

from byov import subprocesses
from byoci.host import config
from byoci.tests.host import (
    assertions,
    fixtures,
)


class TestMonitorConfig(unittest.TestCase):
    """Test master config."""

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)

    def test_defaults(self):
        conf = config.VmStack(None)
        self.assertEqual('selftest', conf.get('byoci'))
        self.assertEqual(self.monitor_name,
                         conf.expand_options('{{byoci}.monitor}'))
        self.assertEqual('/byoci',
                         conf.expand_options('{{byoci}.definition}'))


class TestMonitorSetup(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_setup_succeeds(self):
        fixtures.setup_vm(self, self.master_name)
        fixtures.setup_vm(self, self.monitor_name)
        master_conf = config.VmStack(self.master_name)
        monitor_conf = config.VmStack(self.monitor_name)
        # Ensure monitor knows where to talk to master
        self.assertEqual(master_conf.get('{byoci}.master.api'),
                         monitor_conf.get('{byoci}.master.api'))


class TestMonitorUpdateJobs(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_succeeds(self):
        fixtures.setup_vm(self, self.master_name)
        fixtures.setup_vm(self, self.monitor_name)
        test_cmd = 'cd /byoci && jenkins-jobs update jobs/'
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.monitor_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)


class TestMonitorUpdatePlugins(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_succeeds(self):
        fixtures.setup_vm(self, self.master_name)
        fixtures.setup_vm(self, self.monitor_name)
        test_cmd = 'cd /byoci && ./byo-ci-monitor update-plugins'
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.monitor_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)


class TestMonitorRunJob(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)
        fixtures.setup_vm(self, self.master_name)
        fixtures.setup_vm(self, self.monitor_name)

    def inject_jobs(self):
        # Inject jobs first
        test_cmd = 'cd /byoci && jenkins-jobs update jobs/'
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.monitor_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)

    def test_succeeds(self):
        self.inject_jobs()
        # Now run a known one
        test_cmd = ('cd /byoci &&'
                    ' ./byo-ci-monitor run-job byoci/info-brz-slave-selftest')
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.monitor_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)
        # The job is waiting for a slave (not provisioned here)
        # FIXME: If/when jenkins handling is rewritten as requests-based
        # module, more assertions could be made. -- vila 2018-11-23

    def test_fails(self):
        with self.assertRaises(subprocesses.errors.CommandError) as cm:
            test_cmd = ('cd /byoci &&'
                        ' ./byo-ci-monitor run-job I-dont-exist')
            subprocesses.run(['byov', 'shell', self.monitor_name, test_cmd])
        # because we tunnel through ssh, we get more \n...
        self.assertTrue(
            cm.exception.err.endswith('No job matches I-dont-exist\n\n\n'))

    def test_matches(self):
        self.inject_jobs()
        test_cmd = (
            'cd /byoci &&'
            ' ./byo-ci-monitor run-job -n byoci/info-brz-slave-selftest')
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.monitor_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)
        self.assertEqual('byoci/info-{}\n'.format(self.slave_name), out)

    def test_does_not_match(self):
        self.inject_jobs()
        with self.assertRaises(subprocesses.errors.CommandError) as cm:
            test_cmd = (
                'cd /byoci &&'
                ' ./byo-ci-monitor run-job -n I-dont-exist')
            subprocesses.run(['byov', 'shell', self.monitor_name, test_cmd])
        # 255 says ssh sees an error... maybe some pipe is not closed properly
        # ?  This smells like a FIXME...
        self.assertEqual(255, cm.exception.retcode)
        self.assertEqual('', cm.exception.out)
