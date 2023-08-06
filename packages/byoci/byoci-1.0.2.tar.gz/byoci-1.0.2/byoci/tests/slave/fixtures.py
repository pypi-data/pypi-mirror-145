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
import time


from byoci.slave import (
    config,
    gitlab,
    launchpad,
)
from byoci.tests import fixtures
from byoci.tests.slave import features
from byoci.tests.slave.branches import (
    bzr,
    git,
)
from byov import (
    config as vms_config,
    timeouts,
)


# Useful shortcuts
override_logging = fixtures.override_logging
patch = fixtures.patch
override_env = fixtures.override_env


# Make sure user (or system) defined environment variables do not leak in the
# test environment.
isolated_environ = {
    'HOME': None,
    'BZR_PROGRESS_BAR': None,
}


# The project used for launchpad tests. See 'doc/tests.rst' for the manual (and
# required) steps to bootstrap.
launchpad_test_project_name = 'byoci-test-project'


# The project used for gitlab tests. See 'doc/tests.rst' for the manual (and
# required) steps to bootstrap.
gitlab_test_project_path = 'ci-cd'
gitlab_test_project_name = 'byoci-test-project'


def isolate_from_disk_for_slave(test):
    """Provide an isolated disk-based environment.

    A $HOME directory is setup so tests can setup arbitrary files including
    config ones.
    """
    fixtures.set_uniq_cwd(test)
    # Share the lxd certificate. We could generate one on the fly but assume
    # instead that one is already available since we require the lxc client
    # already.
    lxd_conf_dir = os.path.expanduser('~/.config/lxc')
    # Preserve some options from the outer environment
    outer = config.VmStack(None)
    setup_known_hosts_path = outer.get('byoci.setup_known_hosts')
    lp_login = outer.get('launchpad.login')
    ssh_key = outer.get('ssh.key')
    # Isolate tests from the user environment
    fixtures.isolate_from_env(test, isolated_environ)
    test.home_dir = os.path.join(test.uniq_dir, 'home')
    os.mkdir(test.home_dir)
    fixtures.override_env(test, 'HOME', test.home_dir)
    fixtures.override_env(test, 'BZR_HOME', test.home_dir)
    fixtures.override_env(test, 'LXD_CONF', lxd_conf_dir)
    fixtures.set_bzr_identity(test)
    inner = config.VmStack(None)
    inner.set('byoci', 'selftest')
    # Inject preserved options
    inner.set('byoci.setup_known_hosts', setup_known_hosts_path)
    inner.set('launchpad.login', lp_login)
    inner.set('ssh.key', ssh_key)
    # Also isolate from the system environment
    test.etc_dir = os.path.join(test.uniq_dir,
                                vms_config.system_config_dir()[1:])
    os.makedirs(test.etc_dir)
    fixtures.patch(test, vms_config, 'system_config_dir', lambda: test.etc_dir)
    # Override some options for test purposes (generally the defaults for all
    # byoci workers and as such needing some care for tests to not stomp on
    # each other feet). Also, all expected uses of containers start in a
    # working directory below ~/workspace so mimic that behavior.
    test.workspace = os.path.join(test.home_dir, 'workspace')
    os.mkdir(test.workspace)
    os.chdir(test.workspace)
    return outer, inner


def define_uniq_container(test):
    """To isolate tests from each other, created containers need a unique name.

    To keep those names legal and still user-readable we use the class name and
    the test method name. The process id is added so that the same test suite
    can be run on the same host in several processes.
    """
    container_name = '{}-{}-{}'.format(test.__class__.__name__,
                                       test._testMethodName,
                                       os.getpid())
    # '_' are not valid in hostnames
    test.container_name = container_name.replace('_', '-')
    conf = config.VmStack(test.container_name)
    conf.set('vm.class', 'lxd')
    conf.set('vm.update', 'False')
    conf.set('vm.distribution', 'ubuntu')
    conf.set('vm.release', 'xenial')
    conf.set('vm.architecture', 'amd64')
    conf.store.save()
    conf.store.unload()


def use_launchpad(test, lp_root='production'):
    """Setup environment to use launchpad API and friends."""
    features.test_requires(test, features.launchpad_token)
    # Get original path before isolation
    credentials_path = features.launchpad_token.path
    isolate_from_disk_for_slave(test)
    # Setup to use launchpad API and friends
    conf = config.VmStack(None)
    conf.set('launchpad.service_root', lp_root)
    conf.set('launchpad.credentials', '~/.config/launchpad/{}'.format(lp_root))
    conf.store.save()
    conf.store.unload()
    os.mkdir(os.path.join(test.home_dir, '.config', 'launchpad'))
    with open(credentials_path) as fin:
        with open(conf.get('launchpad.credentials'), 'w') as fout:
            fout.write(fin.read())
    return launchpad.Launchpad(config.VmStack(None))


def use_gitlab(test):
    """Setup environment to use gitlab API and friends."""
    features.test_requires(test, features.gitlab_test_server)
    features.test_requires(test, features.gitlab_token)
    gitlab_vm = features.gitlab_test_server.vm
    # Preserve some options from the outer environment
    # Get original values before isolation
    gitlab_api_url = gitlab_vm.conf.get('gitlab.api.url')
    isolate_from_disk_for_slave(test)
    # Setup to use gitlab API and friends
    conf = config.VmStack(None)
    conf.set('gitlab.api.url', gitlab_api_url)
    conf.set('gitlab.api.credentials', '~/.config/gitlab/credentials')
    for u in ('admin', 'dev', 'reviewer'):
        token = gitlab_vm.conf.get('gitlab.{}.token'.format(u))
        if token is None:
            test.skipTest(
                'gitlab.{}.token missing see doc/secrets.rst'.format(u))
        conf.set('gitlab.{}.token'.format(u), token)
    conf.store.save()
    conf.store.unload()
    os.mkdir(os.path.join(test.home_dir, '.config', 'gitlab'))
    with open(conf.get('gitlab.api.credentials'), 'w') as fout:
        # Most tests impersonate the dev (closest match with rights to land
        # without being admin).
        fout.write(gitlab_vm.conf.get('gitlab.dev.token'))
    test.gl_admin = gitlab.Gitlab(
        config.VmStack(None), gitlab_vm.conf.get('gitlab.admin.token'))
    test.gl_dev = gitlab.Gitlab(
        config.VmStack(None), gitlab_vm.conf.get('gitlab.dev.token'))
    test.gl_reviewer = gitlab.Gitlab(
        config.VmStack(None), gitlab_vm.conf.get('gitlab.reviewer.token'))


class VcsBranchHandler(object):
    """Abstract base class to create local branches."""

    # Must be set by daughter classes
    factory = None
    """The class responsible for handling branches (or repositories)."""
    vcs_dir = None
    """A directory created by the vcs for storing its files."""

    def set_identity(self, test):
        """Setup the vcs identity."""
        raise NotImplementedError(self.set_identify)

    def set_launchpad_access(self, test, lp_root='production'):
        """Setup launchpad access for vcs."""
        raise NotImplementedError(self.set_launchpad_access)

    def lp_branch_url(self, stem):
        """Create a full launchpad url from a stem.

        This should embed the process pid so tests can be run concurrently
        without collision. A single (dedicated but arbitrary) project
        (launchpad_test_project_name) should be used to keep things isolated
        but simple. The MP url is unique as long as a single user doesn't
        attempt to run the test suite from different hosts at the same time and
        is unlucky enough to collide on the process id.

        """
        raise NotImplementedError(self.lp_test_url)

    def get_branch_from_lp(self, lp, url):
        """Get the launchpad object associated with the branch."""
        raise NotImplementedError(self.set_identify)


class BzrBranchHandler(VcsBranchHandler):

    factory = bzr.Branch
    vcs_dir = '.bzr'

    def set_identity(self, test):
        fixtures.set_bzr_identity(test)

    def set_launchpad_access(self, test, lp_root='production'):
        fixtures.set_bzr_launchpad_access(test, lp_root)

    def lp_branch_url(self, stem):
        return 'lp:~{}/{}/{}-{}'.format(
            features.launchpad_identity.identity,
            launchpad_test_project_name,
            stem,
            os.getpid())

    def get_branch_from_lp(self, lp, url):
        return lp.get_bzr_branch(url)


class GitRepositoryHandler(VcsBranchHandler):

    factory = git.Repository
    vcs_dir = '.git'

    def set_identity(self, test):
        fixtures.set_git_identity(test)

    def set_launchpad_access(self, test, lp_root='production'):
        fixtures.set_git_launchpad_access(test, lp_root)

    def lp_branch_url(self, stem):
        return 'lp:~{}/{}/+git/{}-{}'.format(
            features.launchpad_identity.identity,
            launchpad_test_project_name,
            stem,
            os.getpid())

    def get_branch_from_lp(self, lp, url):
        return lp.get_git_repo(url)


# FIXME: Some refactoring is needed to better separate gitlab and launchpad
# as branch providers -- vila 2018-07-24
class GitlabBranchHandler(VcsBranchHandler):

    factory = git.Repository
    vcs_dir = '.git'

    def set_identity(self, test):
        fixtures.set_git_identity(test)

    def set_gitlab_access(self, test):
        fixtures.set_gitlab_access(test)

    def get_project_name(self):
        # FIXME: features.gitlab_identity.identify instead of
        # gitlab_test_project_path ? -- vila 2018-07-25
        return '{}/{}'.format(gitlab_test_project_path,
                              gitlab_test_project_name)

    def gl_branch_url(self, stem):
        url = 'gitlab:{}'.format(self.get_project_name())
        branch_name = '{}-{}'.format(stem, os.getpid())
        return url, branch_name

    def get_branch_from_gl(self, gl, project, branch):
        return gl.get_branch(project, branch)


class VcsProposalHandler(object):
    """Abstract base class to interact with proposals."""

    def create(self, test, source, target, message, cover=None):
        """Create a merge proposal of source into target."""
        raise NotImplementedError(self.create_proposal)

    def build_comment_subject(self, proposal):
        """Build a standard subject for proposal comment."""
        raise NotImplementedError(self.build_comment_subject)


class BzrProposalHandler(VcsProposalHandler):

    def create(self, test, proposed, target, message, cover=None):
        if cover is None:
            cover = message
        return proposed.createMergeProposal(
            target_branch=target,
            initial_comment=cover,
            commit_message=message,
            needs_review=True)

    # FIXME: duplicated in LandApprovedBzrProposal.proposal_comment_subject
    # -- vila 2017-01-25
    def build_comment_subject(self, proposal):
        # Uses display_name (lp:xxx)
        return 'Re: [Merge] {} into {}'.format(
            proposal.source_branch.display_name,
            proposal.target_branch.display_name)


class GitProposalHandler(VcsProposalHandler):

    def get_ref(self, test, repo, branch):
        ref = repo.getRefByPath(path=branch)
        # Wait before giving up, this should be enough to cover
        # small maintenance windows or significant slowdowns.
        sleeps = timeouts.ExponentialBackoff(2, 600, 12)
        for sleep in sleeps:
            if ref is not None:
                break
            time.sleep(sleep)
            ref = repo.getRefByPath(path='master')
        try:
            test.assertIsNot(None, ref,
                             'Branch {} cannot be found inside {}'.format(
                                 branch, repo.unique_name))
        except AssertionError:
            # FIXME: Strictly speaking this should be an expected failure but
            # that will do for now -- vila 2018-01-17
            test.skipTest('launchpad git backend is broken')
        return ref

    def create(self, test, proposed, target, message, cover=None):
        if cover is None:
            cover = message
        proposed_git_ref = self.get_ref(test, proposed, 'master')
        test.assertEqual('refs/heads/master', proposed_git_ref.path)
        target_git_ref = self.get_ref(test, target, 'master')
        test.assertEqual('refs/heads/master', target_git_ref.path)
        return proposed_git_ref.createMergeProposal(
            merge_target=target_git_ref,
            initial_comment=cover,
            commit_message=message,
            needs_review=True)

    # FIXME: duplicated in LandApprovedGitProposal.proposal_comment_subject
    # -- vila 2017-01-25
    def build_comment_subject(self, proposal):
        # Uses unique_name (xxx)
        proposed_url = '{}:{}'.format(
            proposal.source_git_repository.unique_name,
            proposal.source_git_path[len('refs/heads/'):])
        target_url = '{}:{}'.format(
            proposal.target_git_repository.unique_name,
            proposal.target_git_path[len('refs/heads/'):])
        return 'Re: [Merge] {} into {}'.format(
            proposed_url,
            target_url)


class GitlabProposalHandler(VcsProposalHandler):

    def create(self, test, proposed, target, message, cover=None):
        if cover is None:
            cover = message
        return test.gl_dev.create_proposal(
            test.target_project_name, proposed, target, title=proposed,
            description=cover)

    # FIXME: duplicated in LandApprovedGitlabProposal.proposal_comment_subject
    # -- vila 2018-08-01
    def build_comment_subject(self, proposal):
        # gitlab doesn't expose the mail subject
        return ''


def setup_proposal_target(test):
    """Create a local target branch to build proposals."""
    branch = test.branch_handler.factory('target')
    test.addCleanup(branch.delete)
    branch.create()
    branch.update('Something', 'file: foo\nfoo content\n')
    test.target_url = test.branch_handler.lp_branch_url('target')
    branch.push(test.target_url)
    test.target_lp_branch = test.branch_handler.get_branch_from_lp(
        test.lp, test.target_url)
    test.assertIsNot(None, test.target_lp_branch)
    test.addCleanup(test.target_lp_branch.lp_delete)


def setup_gitlab_proposal_target(test):
    """Create a local target branch to build proposals."""
    branch = test.branch_handler.factory('target')
    test.addCleanup(branch.delete)
    branch.create()
    branch.update('Something', 'file: foo\nfoo content\n')
    (test.target_url,
     test.target_branch_name) = test.branch_handler.gl_branch_url('target')
    # FIXME: switch() shouldn't be necessary -- vila 2018-07-25
    branch.switch(test.target_branch_name)
    branch.push(test.target_url, test.target_branch_name)
    test.target_project_name = test.branch_handler.get_project_name()
    test.target_project = test.gl_dev.get_project(test.target_project_name)
    test.target_gl_branch = test.branch_handler.get_branch_from_gl(
        test.gl_dev, test.target_project_name, test.target_branch_name)
    test.assertIsNot(None, test.target_gl_branch)
    test.addCleanup(
        test.gl_dev.delete_branch, test.target_project_name,
        test.target_branch_name)


def create_proposal(test, name, approved=False, commit_msg=None, cover=None):
    """Create a merge proposal from a branch.

    :param test: A test case with a 'proposal_handler', 'branch_handler',
        'target_url' and 'target_lp_branch' attributes. A 'proposed_lp_branch'
        attribute will be created. See setup_proposal_target() to create
        'target_url' and 'target_lp_branch'.

    :param name: The branch name.

    :param approved: Should the proposal be approved.

    :param commit_msg: Commit message for the proposal. A default one is
        created if None is provided.

    :param cover: The cover letter for the proposal. Defaults to commit message
        if None is provided.

    """
    proposed = test.branch_handler.factory(name)
    # Strictly speaking we should create from the lp branch but we just
    # pushed 'target' there so this avoids a useless roundtrip.
    proposed.create_from('target')
    vcs_commit_msg = '{} purpose'.format(name)
    if commit_msg is None:
        commit_msg = vcs_commit_msg
    if cover is None:
        cover = commit_msg
    proposed.update(vcs_commit_msg,
                    'file: {}\n{} content\n'.format(name, name))
    proposed_lp_url = test.branch_handler.lp_branch_url(name)
    proposed.push(proposed_lp_url)
    test.proposed_lp_branch = test.branch_handler.get_branch_from_lp(
        test.lp, proposed_lp_url)
    test.addCleanup(test.proposed_lp_branch.lp_delete)
    proposal = test.proposal_handler.create(
        test, test.proposed_lp_branch, test.target_lp_branch,
        commit_msg, cover)
    if approved:
        subject = test.proposal_handler.build_comment_subject(proposal)
        proposal.createComment(subject=subject, vote='Approve',
                               content='Well done!')
        proposed_rev_id = proposed.tip_commit_id()
        proposal.setStatus(status='Approved', revid=proposed_rev_id)
    return proposal


def create_gitlab_proposal(test, name, approved=False, commit_msg=None,
                           cover=None):
    """Create a merge proposal from a branch.

    :param test: A test case with a 'proposal_handler', 'branch_handler',
        'target_url' and 'target_branch_name' attributes. 'proposed_url' and
        'proposed_branch_name' attributes will be created. See
        setup_proposal_target() to create 'target_url' and
        'target_branch_name'.

    :param name: The branch name.

    :param approved: Should the proposal be approved.

    :param commit_msg: Commit message for the proposal. A default one is
        created if None is provided.

    :param cover: The cover letter for the proposal. Defaults to commit message
        if None is provided.

    """
    proposed = test.branch_handler.factory(name)
    # Strictly speaking we should create from the gitlab branch but we just
    # pushed 'target' there so this avoids a useless roundtrip.
    proposed.create_from('target')
    vcs_commit_msg = '{} purpose'.format(name)
    if commit_msg is None:
        commit_msg = vcs_commit_msg
    if cover is None:
        cover = commit_msg
    proposed.update(vcs_commit_msg,
                    'file: {}\n{} content\n'.format(name, name))
    (proposed_url,
     proposed_branch_name) = test.branch_handler.gl_branch_url(name)
    # FIXME: switch() shouldn't be necessary -- vila 2018-07-25
    proposed.switch(proposed_branch_name)
    proposed.push(proposed_url, proposed_branch_name)
    test.addCleanup(
        # FIXME: proposed_project_name would be cleaner even if that's the same
        # project anyway -- vila 2018-07-25
        test.gl_dev.delete_branch, test.target_project_name,
        proposed_branch_name)
    test.proposed_gl_branch = test.branch_handler.get_branch_from_gl(
        test.gl_dev, test.target_project_name, proposed_branch_name)
    proposal = test.proposal_handler.create(
        test, proposed_branch_name, test.target_branch_name,
        commit_msg, cover)
    test.addCleanup(
        test.gl_admin.delete_proposal, test.target_project_name,
        proposal['iid'])
    if approved:
        test.gl_reviewer.create_proposal_comment(
            test.target_project_name,
            proposal['iid'], 'Good stuff\n/award :+1:')
        test.gl_dev.mark_proposal(test.target_project_name, proposal['iid'],
                                  'tests-pass')
        proposal = test.gl_dev.get_proposal(test.target_project_name,
                                            proposal['iid'])
    return proposal


# Useful shortcuts to export but not used internally
set_bzr_launchpad_access = fixtures.set_bzr_launchpad_access
