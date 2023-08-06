# This file is part of Build Your Own CI
#
# Copyright 2017, 2018 Vincent Ladeuil
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

from byoci.host import config
from byov import subprocesses
from byoci.tests.host import (
    assertions,
    fixtures,
)


class TestMasterConfig(unittest.TestCase):
    """Test master config."""

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)

    def test_defaults(self):
        conf = config.VmStack(self.master_name)
        self.assertEqual('selftest', conf.get('byoci'))
        self.assertEqual(self.master_name,
                         conf.expand_options('{{byoci}.master}'))
        self.assertEqual(conf.expand_options('{jenkins.home}/tokens'),
                         conf.expand_options('{jenkins.tokens}'))


class TestMasterSetup(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_setup_succeeds(self):
        fixtures.setup_vm(self, self.master_name)
        conf = config.VmStack(self.master_name)
        mat_path = os.path.join(
            os.path.expanduser(conf.get('jenkins.tokens')),
            'monitor-api-token')
        test_cmd = 'test -f ' + mat_path
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.master_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)


class TestMasterSlave(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_ssh_to_slave(self):
        fixtures.setup_vm(self, self.master_name)
        fixtures.setup_vm(self, self.slave_name)
        sconf = config.VmStack(self.slave_name)
        test_cmd = sconf.expand_options(
            # The master is authorized (the name of the key is used as the
            # comment so we check that).
            'grep {{byoci}.master.ssh.key} ~/.ssh/authorized_keys')
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.slave_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)
        # And now we connect from master to slave to really exercise the whole
        # path.
        mconf = config.VmStack(self.master_name)
        kls = mconf.get('vm.class')
        master = kls(mconf)
        ret, out, err = master.shell_captured(
            'ssh -v {} whoami'.format(self.slave_name))
        self.assertEqual(0, ret)
        self.assertEqual(sconf.get('vm.user'), out.strip())
