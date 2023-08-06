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

import os
import io
import unittest


import byov
from byoci.tests.host import fixtures
from byov import subprocesses


HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


class TestSetup(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_succeeds(self):
        self.addCleanup(fixtures.teardown_vm, self, self.slave_name)
        self.addCleanup(fixtures.teardown_vm, self, self.monitor_name)
        self.addCleanup(fixtures.teardown_vm, self, self.master_name)

        cmd = subprocesses.which('setup/byoci', byov.path)
        self.assertTrue(cmd is not None)
        ret, out, err = subprocesses.run([cmd, 'selftest'])
        self.assertEqual(0, ret)
