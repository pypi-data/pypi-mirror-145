# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil.
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

from byoci.monitor import config
from byoci.tests.monitor import (
    features,
    fixtures,
)


class TestMonitorStack(unittest.TestCase):
    """Test config option values."""

    def setUp(self):
        super().setUp()
        features.test_requires(self, features.master_credentials)
        fixtures.isolate_from_disk_for_monitor(self)

    def test_defaults(self):
        conf = config.MonitorStack()
        # Options are set, we don't know the values, just a smoke test
        conf.expand_options('{byoci.api}')
        conf.expand_options('{byoci.user}')
        conf.expand_options('{byoci.token}')
        conf.expand_options('{jenkins.home}')
