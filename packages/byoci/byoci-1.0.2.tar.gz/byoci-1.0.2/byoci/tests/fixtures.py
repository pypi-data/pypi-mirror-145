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

import io
import logging
import os


from byoci.tests import features
from byot import fixtures
from byov import subprocesses


# Useful shortcuts
set_uniq_cwd = fixtures.set_uniq_cwd
build_tree = fixtures.build_tree
patch = fixtures.patch
isolate_from_env = fixtures.isolate_from_env
override_env = fixtures.override_env


def override_logging(test, stream_out=None,
                     level=logging.INFO, fmt='%(message)s'):
    """Setup a logging handler, restoring the actual handlers after the test.

    This assumes a logging setup where handlers are added to the root logger
    only.

    :param stream_out: A stream where log messges will be recorded.

    :param level: The logging level to be active during the test.

    :param fmt: The logging format to use during the test.

    """
    if stream_out is None:
        stream_out = io.StringIO()
        test.log_stream = stream_out
    root_logger = logging.getLogger(None)
    # Using reversed() below ensures we can modify root_logger.handlers as well
    # as providing the handlers in the right order for cleanups.
    for handler in reversed(root_logger.handlers):
        root_logger.removeHandler(handler)
        test.addCleanup(root_logger.addHandler, handler)
    # Install the new handler
    new_handler = logging.StreamHandler(stream_out)
    test.addCleanup(root_logger.removeHandler, new_handler)
    root_logger.addHandler(new_handler)
    # Install the new level, restoring the actual one after the test
    test.addCleanup(root_logger.setLevel, root_logger.level)
    root_logger.setLevel(level)


def set_bzr_identity(test):
    """Set the bzr whoami."""
    features.test_requires(test, features.bzr_identity)
    test.assertTrue(test.uniq_dir in os.environ['HOME'])
    subprocesses.run(['bzr', 'whoami', features.bzr_identity.identity])


def set_git_identity(test):
    """Set the git user name and email."""
    features.test_requires(test, features.git_identity)
    test.assertTrue(test.uniq_dir in os.environ['HOME'])
    subprocesses.run(['git', 'config', '--global', 'user.name',
                      features.git_identity.name])
    subprocesses.run(['git', 'config', '--global', 'user.email',
                      features.git_identity.email])


def set_bzr_launchpad_access(test, lp_root):
    """Set the bzr launchpad login."""
    features.test_requires(test, features.launchpad_identity)
    test.assertTrue(test.uniq_dir in os.environ['HOME'])
    if lp_root == 'qastaging':
        # All tests did run against qastaging in the past, keep the code for
        # reference -- vila 2018-07-23
        plugin_dir = os.path.join(test.uniq_dir, 'home', '.bazaar', 'plugins')
        os.makedirs(plugin_dir)
        with open(os.path.join(plugin_dir, 'qastagingonly.py'), 'w') as f:
            f.write('from bzrlib.plugins.launchpad import lp_directory\n')
            f.write('lp_directory.LaunchpadService.DEFAULT_INSTANCE'
                    ' = "{}"'.format(lp_root))
    subprocesses.run(['bzr', 'launchpad-login',
                      features.launchpad_identity.identity])


def set_git_launchpad_access(test, lp_root):
    """Configure git to access launchpad."""
    features.test_requires(test, features.launchpad_identity)
    test.assertTrue(test.uniq_dir in os.environ['HOME'])
    if lp_root == 'production':
        git_host = 'git.launchpad.net'
    elif lp_root == 'qastaging':
        git_host = 'git.qastaging.paddev.net'
    subprocesses.run(
        ['git', 'config', '--global',
         'url.ssh://{}@{}/.insteadOf'.format(
             features.launchpad_identity.identity,
             git_host),
         'lp:'])
    subprocesses.run(
        ['git', 'config', '--global', 'push.default', 'simple'])


def set_gitlab_access(test):
    """Configure git to access gitlab."""
    features.test_requires(test, features.gitlab_identity)
    test.assertTrue(test.uniq_dir in os.environ['HOME'])
    git_host = features.gitlab_test_server.vm.conf.get('vm.ip')
    subprocesses.run(
        ['git', 'config', '--global',
         'url.ssh://git@{}/.insteadOf'.format(git_host),
         'gitlab:'])
    subprocesses.run(
        ['git', 'config', '--global', 'push.default', 'simple'])
    git_ssh_options = features.gitlab_test_server.vm.conf.get('ssh.options')
    # The following requires git >= 2.10
    # subprocesses.run(
    #     ['git', 'config', '--global',
    #      'core.sshCommand', 'ssh {}'.format(' '.join(git_ssh_options))])
    fixtures.override_env(test, 'GIT_SSH_COMMAND',
                          'ssh {}'.format(' '.join(git_ssh_options)))
