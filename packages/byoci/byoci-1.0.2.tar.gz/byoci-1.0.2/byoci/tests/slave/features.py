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

from byoci.slave import config
from byoci.tests import features
from byov.tests import features as vms_features


HERE = os.path.abspath(os.path.dirname(__file__))


ssh_agent_feature = features.ExecutableFeature('ssh-agent')


class LaunchpadToken(features.Feature):
    """Credentials for launchpad."""

    def __init__(self, lp_root='production'):
        super().__init__()
        if features.on_slave.available():
            # FIXME: Not tested :-/ -- vila 2018-10-20
            conf = config.VmStack('localhost')
            self.path = os.path.join(conf.expand_options('{{byoci}.secrets}'),
                                     'launchpad', lp_root)
        else:
            conf = config.VmStack(None)
            # {selftest.host.secrets} is not setup yet, use testing instead
            self.path = os.path.join(
                conf.expand_options('{testing.host.secrets}'),
                'launchpad', lp_root)

    def _probe(self):
        # We only test that the credentials file exists here, not its validity.
        return os.path.exists(self.path)

    def feature_name(self):
        return 'An OAuth token in {} for qastaging launchpad'.format(self.path)


# Parametrizing tests to run against production and qastaging starts here:
# launchpad_token is a singleton. It shouldn't. There should be one for
# production and one for qastaging. And controlled by a user option in a
# .conf-tests file.
launchpad_token = LaunchpadToken()


class GitlabToken(features.Feature):
    """Credentials for gitlab."""

    def __init__(self):
        super().__init__()
        if features.on_slave.available():
            conf = config.VmStack('localhost')
            self.path = os.path.join(conf.expand_options('{{byoci}.secrets}'),
                                     'gitlab', 'credentials')
        else:
            conf = config.VmStack(None)
            # {selftest.host.secrets} is not setup yet, use testing instead
            self.path = os.path.join(
                conf.expand_options('{testing.host.secrets}'),
                'gitlab', 'credentials')

    def _probe(self):
        # We only test that the credentials file exists here, not its validity.
        return os.path.exists(self.path)

    def feature_name(self):
        return 'An private token in {} for gitlab'.format(self.path)


gitlab_token = GitlabToken()


# Features relying on an environment property should be checked before any test
# isolation is setup. Once this is done, they can be freely used to decorate
# tests [classes] or during setUp().

launchpad_token.available()
gitlab_token.available()
ssh_agent_feature.available()


# Useful shortcuts to export but not used internally
requires_existing_vm = vms_features.requires_existing_vm
ssh_feature = vms_features.ssh_feature
tests_config = vms_features.tests_config
requires = features.requires
test_requires = features.test_requires
bzr_identity = features.bzr_identity
git_identity = features.git_identity
launchpad_identity = features.launchpad_identity
gitlab_identity = features.gitlab_identity
gitlab_test_server = features.gitlab_test_server
