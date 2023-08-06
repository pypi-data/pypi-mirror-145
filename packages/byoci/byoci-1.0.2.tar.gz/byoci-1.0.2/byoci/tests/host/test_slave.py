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

from byoci.host import config
from byov import subprocesses
from byoci.tests.host import (
    assertions,
    fixtures,
)


class TestSlaveConfig(unittest.TestCase):
    """Test slave config."""

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)

    def test_defaults(self):
        conf = config.VmStack(self.slave_name)
        self.assertEqual('selftest', conf.get('byoci'))
        # A single slave will do
        self.assertEqual(self.slave_name,
                         conf.expand_options('{{byoci}.slaves}'))


class TestSlaveSetup(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        import logging
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self, level=logging.DEBUG)

    def test_setup_succeeds(self):
        fixtures.setup_vm(self, self.master_name)
        fixtures.setup_vm(self, self.slave_name)
        conf = config.VmStack(self.slave_name)
        test_cmd = conf.expand_options(
            # The slave private ssh key has been installed
            'test -f ~/.ssh/{{byoci}.slave.ssh.key}')
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.slave_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)
        test_cmd = 'test -f ~/.config/byov/conf.d/byov-localhost.conf'
        ret, out, err = subprocesses.run(
            ['byov', 'shell', self.slave_name, test_cmd])
        assertions.assertShellSuccess(self, test_cmd, ret, out, err)
