# This file is part of Build Your Own CI
#
# Copyright 2017, 2018 Vincent Ladeuil
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

import os
import re

from byoc import errors
from byot import features
from byov import (
    config,
    subprocesses,
)

HERE = os.path.abspath(os.path.dirname(__file__))

lxd_client_feature = features.ExecutableFeature('lxc')
make_feature = features.ExecutableFeature('make')
flake8_feature = features.ExecutableFeature('flake8')


class OnHost(features.Feature):
    """Is the current process running on a host whose name matches a regexp."""

    def __init__(self, hostname_regexp):
        super().__init__()
        self.hostname_regexp = hostname_regexp
        self.compiled_re = re.compile(hostname_regexp)

    def _probe(self):
        return self.compiled_re.search(os.uname().nodename) is not None

    def feature_name(self):
        return 'Running on a hostname matching {}'.format(self.hostname_regexp)


on_monitor = OnHost('^brz-monitor')
on_slave = OnHost('^brz-slave-')


class BzrIdentity(features.Feature):
    """A feature capturing the current bzr whoami."""

    def __init__(self):
        super().__init__()
        self.identify = None

    def _probe(self):
        try:
            # 'cd ~' is needed for the edge case where the current directory is
            # a branch in a mounted file system that doesn't include the
            # associated (shared) repository. This happens for the
            # brz-slave-testing container when running the slave tests.  There
            # is no other use case that is known to make 'bzr whoami' fail
            # complaining that there is no repository around ;)
            _, out, _ = subprocesses.run(['sh', '-c', 'cd ~ && bzr whoami'])
            self.identity = out.strip()
            return True
        except subprocesses.errors.CommandError:
            return False

    def feature_name(self):
        return 'An existing bazaar whoami'


bzr_identity = BzrIdentity()


class GitIdentity(features.Feature):
    """A feature capturing the current git user email."""

    def __init__(self):
        super().__init__()
        self.name = None
        self.email = None

    def _probe(self):
        try:
            _, out, _ = subprocesses.run(['git', 'config', 'user.name'])
            self.name = out.strip()
            _, out, _ = subprocesses.run(['git', 'config', 'user.email'])
            self.email = out.strip()
            return True
        except subprocesses.errors.CommandError:
            return False

    def feature_name(self):
        return 'An existing git user name and email'


git_identity = GitIdentity()


class LaunchpadIdentity(features.Feature):
    """A feature capturing the current bzr launchpad login."""

    def __init__(self):
        super().__init__()
        self.identity = None

    def _probe(self):
        try:
            _, out, _ = subprocesses.run(['bzr', 'launchpad-login'])
            self.identity = out.strip()
            return True
        except subprocesses.errors.CommandError:
            return False

    def feature_name(self):
        return 'An existing launchpad login'


launchpad_identity = LaunchpadIdentity()


class GitlabIdentity(features.Feature):
    """A feature capturing the current gitlab login."""

    def __init__(self):
        super().__init__()
        self.identity = None

    def _probe(self):
        try:
            _, out, _ = subprocesses.run(['git', 'config', 'gitlab.login'])
            self.identity = out.strip()
            return True
        except subprocesses.errors.CommandError:
            return False

    def feature_name(self):
        return 'An existing gitlab login'


gitlab_identity = GitlabIdentity()


# FIXME: backport to byov accepting as a RunningVM with a vm_name parameter
# -- vila 2018-07-29
class GitlabTestServer(features.Feature):

    def __init__(self):
        super().__init__()
        self.vm = None

    def _probe(self):
        try:
            conf = config.VmStack('gitlab')
            try:
                kls = conf.get('vm.class')
            except errors.OptionMandatoryValueError:
                return False
            if isinstance(kls, str):
                # FIXME: monitor doesn't have byov properly imported so the vm
                # classes registry is not available. Punting for now
                # -- vila 2018-10-21
                return False
            # FIXME: Some classes may require more features (lxd for one)
            # -- vila 2018-07-29
            self.vm = kls(conf)
            if self.vm.state() != 'RUNNING':
                return False
            return True
        except subprocesses.errors.CommandError:
            return False

    def feature_name(self):
        return 'A running gitlab server'


gitlab_test_server = GitlabTestServer()

# Features relying on an environment property should be checked before any test
# isolation is setup. Once this is done, they can be freely used to decorate
# tests [classes] or during setUp().

bzr_identity.available()
git_identity.available()
launchpad_identity.available()
gitlab_identity.available()
gitlab_test_server.available()
lxd_client_feature.available()
make_feature.available()
flake8_feature.available()
on_monitor.available()
on_slave.available()

# Useful shortcuts to export but not used internally
ExecutableFeature = features.ExecutableFeature
Feature = features.Feature
requires = features.requires
test_requires = features.test_requires
