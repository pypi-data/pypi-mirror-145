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
import os

from byoc import errors
from byoci.monitor import config
from byoci.tests import features


HERE = os.path.abspath(os.path.dirname(__file__))


class MasterCredentials(features.Feature):

    def _probe(self):
        try:
            conf = config.MonitorStack()
            conf.get('byoci.api')
            conf.get('byoci.user')
            conf.get('byoci.token')
        except errors.OptionMandatoryValueError:
            return False
        return True

    def feature_name(self):
        return 'A valid set of byoci master credentials'


master_credentials = MasterCredentials()

# Features relying on an environment property should be checked before any test
# isolation is setup. Once this is done, they can be freely used to decorate
# tests [classes] or during setUp().

# Keeping the vm up to date and in sync with the working tree is the dev
# responsibility.
# Tests are isolated though so they must not break such a vm nor leak in any
# way.

# FIXME: Almost there but requires_existing_vm() doc says it needs to be called
# after fixtures.setup_tests_config(). It may be still possible to call it now
# with a slightly different semantic (outside context rather than isolated test
# context) -- vila 2018-02-10

# monitor_vm = requires_existing_vm('brz-monitor-testing')
# monitor_vm.available()

master_credentials.available()

# Useful shortcuts to export but not use internally
requires = features.requires
test_requires = features.test_requires
