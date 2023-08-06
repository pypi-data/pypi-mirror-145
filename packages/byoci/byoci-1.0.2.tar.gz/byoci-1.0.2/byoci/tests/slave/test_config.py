# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2016, 2017 Canonical Ltd.
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

import unittest

from byoci.slave import config
from byoci.tests.slave import fixtures


class TestVmStack(unittest.TestCase):
    """Test config option values."""

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)

    def test_defaults(self):
        conf = config.VmStack(None)
        self.assertEqual('production', conf.get('launchpad.service_root'))
        self.assertTrue(conf.get('launchpad.credentials').endswith(
            '/launchpad/production'))

    def test_test_config(self):
        conf = config.VmStack(None)
        conf.set('launchpad.service_root', 'qastaging')
        conf.set('launchpad.credentials',
                 '~/.config/byov/launchpad-qastaging')
        conf.store.save_changes()
        # Create a new stack
        conf2 = config.VmStack(None)
        self.assertEqual('qastaging', conf2.get('launchpad.service_root'))
