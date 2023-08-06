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


import logging
import os
import sys

import byoci


from byov import (
    errors,
    subprocesses,
)


from byoci import commands
from byoci.slave import (
    config,
    containers,
    gitlab,
    launchpad,
)


logger = logging.getLogger(__name__)


setup_logging = commands.setup_logging


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


class ArgParser(commands.ArgParser):
    """An argument parser for the byo-ci-slave script."""

    script_name = 'byo-ci-slave'


# All commands are registered here, defining what run() supports
command_registry = commands.CommandRegistry()


class Help(commands.Help):

    description = 'Describe byo-ci-slave commands.'
    command_registry = command_registry
    arg_parser_class = ArgParser


command_registry.register(Help)


class Command(commands.Command):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            '--option', '-O', metavar='OPTION=VALUE',
            action='append', dest='overrides', default=[],
            help='Override OPTION with provided VALUE. Can be repeated.')
        self.conf = config.VmStack(None)

    def parse_args(self, args):
        super().parse_args(args)
        self.conf.cmdline_store.from_cmdline(self.options.overrides)
        # Now we may configure logging. It can't be configured until we reach
        # this point, this means errors occuring before this point can be
        # logged without the user specified options.
        log_level = self.conf.get('logging.level')
        log_format = self.conf.get('logging.format')
        commands.setup_logging(log_level, log_format)
        return self.options


class SetupTree(Command):

    # Daughters classes should set the following:
    name = None
    description = None
    source_help = None
    vcs_cmd_name = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'source', metavar='SOURCE',
            help=self.source_help)
        self.parser.add_argument(
            'path', metavar='PATH',
            help='Path to the resulting tree.')

    def vcs(self, args):
        try:
            vcs_cmd = [self.vcs_cmd_name] + args
            return subprocesses.run(vcs_cmd)
        except errors.CommandError:
            logger.exception('{} failed'.format(' '.join(vcs_cmd)))
            raise

    def setup_tree(self):
        """Setup a tree in a specified directory.

        :param work_dir: Path to install the branch at.
        """
        logger.debug('Setting up [{}]'.format(self.options.path))
        # Inherited by daughter classes, cleanup first.
        if os.path.exists(self.options.path):
            logger.debug('Removing [{}]'.format(self.options.path))
            subprocesses.run(['rm', '-fr', self.options.path])

    def run(self):
        self.setup_tree()
        return 0


class SetupBzrTree(SetupTree):

    name = 'setup-bzr-tree'
    description = 'Setup a brz working tree.'
    source_help = 'The bazaar branch url.'
    vcs_cmd_name = 'bzr'

    def bzr(self, args):
        return self.vcs(args)

    def setup_tree(self):
        super().setup_tree()
        logger.debug('Setting up [{}] with bzr'.format(self.options.path))
        if not os.path.exists(self.options.path):
            parent = os.path.dirname(self.options.path)
            if parent:
                # Provide the parent directory
                logger.debug('Providing [{}]'.format(self.options.path))
                ensure_dir(parent)
        return self.bzr(['branch', self.options.source, self.options.path])


command_registry.register(SetupBzrTree)


class SetupGitTree(SetupTree):

    name = 'setup-git-tree'
    description = 'Setup a git workingtree.'
    source_help = ("The git repo url (can be suffixed with ';<branch>',"
                   " master otherwise).")
    vcs_cmd_name = 'git'

    def parse_args(self, args):
        super().parse_args(args)
        if ';' in self.options.source:
            (self.options.source,
             self.options.branch) = self.options.source.split(';')
        else:
            self.options.branch = 'master'
        return self.options

    def git(self, args):
        return self.vcs(args)

    def setup_tree(self):
        super().setup_tree()
        logger.debug('Setting up [{}] with git'.format(self.options.path))
        self.git(['clone', self.options.source, self.options.path])
        with byoci.working_directory(self.options.path):
            self.git(['checkout', self.options.branch])


command_registry.register(SetupGitTree)


class ApprovedBzrProposals(Command):

    name = 'approved-bzr-proposals'
    description = 'Check for approved bzr merge proposals.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'target', metavar='TARGET',
            help='The bazaar target branch for the merge proposals.')

    def run(self):
        self.lp = launchpad.Launchpad(self.conf)
        target_branch = self.lp.get_bzr_branch(self.options.target)
        if target_branch is None:
            logger.error('{} is not a bzr branch'.format(
                self.options.target))
            return 1
        logger.info('Searching proposals for {}'.format(
            target_branch.web_link))
        for proposal in target_branch.landing_candidates:
            logger.info('Looking at {}'.format(proposal.web_link))
            unique_name = proposal.target_branch.unique_name
            if unique_name != target_branch.unique_name:
                logger.info('Ignoring, target is {}'.format(
                    unique_name))
                continue
            queue_status = proposal.queue_status
            if queue_status != 'Approved':
                logger.info('Ignoring, status is {}'.format(queue_status))
                continue
            # The proposal is approved
            logger.info('{} is approved'.format(proposal.web_link))
            return 0
        # None of the proposals are approved
        logger.error('No proposal is approved')
        return 1


command_registry.register(ApprovedBzrProposals)


class ApprovedGitProposals(Command):

    name = 'approved-git-proposals'
    description = 'Check for approved git merge proposals.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIXME: Shouldn't we mention the branch inside the repository there ?
        # Even if defaulting to 'master' -- vila 2016-12-07
        self.parser.add_argument(
            'target', metavar='TARGET',
            help='The target git repository for the merge proposals.')

    def run(self):
        self.lp = launchpad.Launchpad(self.conf)
        target_git_repo = self.lp.get_git_repo(self.options.target)
        if target_git_repo is None:
            logger.error('{} is not a git repository'.format(
                self.options.target))
            return 1
        for proposal in target_git_repo.landing_candidates:
            logger.info('Looking at {}'.format(proposal.web_link))
            unique_name = proposal.target_git_repository.unique_name
            if unique_name != target_git_repo.unique_name:
                logger.info('Ignoring, target is {}'.format(
                    unique_name))
                continue
            queue_status = proposal.queue_status
            if queue_status != 'Approved':
                logger.info('Ignoring, status is {}'.format(queue_status))
                continue
            # The proposal is approved
            logger.info('{} is approved'.format(proposal.web_link))
            return 0
        # None of the Proposals are approved
        logger.error('No proposal is approved')
        return 1


command_registry.register(ApprovedGitProposals)


def is_gitlab_proposal_approved(proposal):
    # The proposal needs to be tested and approved
    if 'tests-pass' not in proposal['labels']:
        logger.info('Ignoring, not tested yet')
        return False
    if proposal['downvotes'] != 0:
        logger.info('Ignoring, {} down votes'.format(
            proposal['downvotes']))
        return False
    if not proposal['upvotes'] >= 1:
        logger.info('Ignoring, not enough up votes ({})'.format(
            proposal['upvotes']))
        return False
    # FIXME: What if the proposal was rejected when attempting to land ?
    # -- vila 2018-08-01
    # FIXME: WIPs should be skipped too -- vila 2018-08-01
    return True


class ApprovedGitlabProposals(Command):

    name = 'approved-gitlab-proposals'
    description = 'Check for approved gitlab merge proposals.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'target', metavar='TARGET',
            help='The target git repository for the merge proposals.')

    def parse_args(self, args):
        super().parse_args(args)
        if ';' in self.options.target:
            (self.options.target,
             self.options.branch) = self.options.target.split(';')
        else:
            self.options.branch = 'master'
        return self.options

    def run(self):
        self.gl = gitlab.Gitlab(self.conf)
        proposals = self.gl.get_proposals(self.options.target,
                                          self.options.branch)
        for proposal in proposals:
            logger.info('Looking at {}'.format(proposal['web_url']))
            if proposal['target_branch'] != self.options.branch:
                logger.info('Ignoring, target is {}'.format(
                    proposal['target_branch']))
                continue
            if not is_gitlab_proposal_approved(proposal):
                continue
            # The proposal is approved
            logger.info('{} is approved'.format(proposal['web_url']))
            return 0
        # None of the Proposals are approved
        logger.error('No proposal is approved')
        return 1


command_registry.register(ApprovedGitlabProposals)


class CommandWithContainer(Command):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # The container where commands are run
        self.worker = None

    # FIXME: 'mounts' and 'remote_work_dir' should be options. This defines the
    # file systems shared between the slave and the vms.  -- vila# 2018-05-18
    def get_mounts_and_remote(self, local_dir):
        """Build mount points and remote working directory.

        :param local_dir: The local directory needed inside the worker.

        :return: A (mounts, remote) tuple where 'mounts' is a list of mount
            points and 'remote' the absolute path for the directory inside the
            container.
        """
        mounts = ['~/workspace:/workspace']
        rel_path = os.path.relpath(
            local_dir,
            os.path.realpath(os.path.expanduser('~/workspace')))
        # FIXME: Arguably a more restricted view should be exposed but at least
        # the slave home directory is not exposed in the container.
        # -- vila 2017-02-07
        remote_work_dir = os.path.join('/workspace', rel_path)
        return mounts, remote_work_dir

    def create_worker(self, backing_container_name, name=None,
                      mounts=None):
        """Create and start a worker.

        :param backing_container_name: The base container defined in
            byov.conf.

        :param name: The worker name (defaults to worker-<base name>-<pid> if
            not specified').

        :params mounts: An optional list of mount '<local>:<remote>' pairs.

        """
        if name is None:
            name = 'worker-{}-{}'.format(backing_container_name, os.getpid())
        worker = containers.Worker(name, backing_container_name,
                                   out=self.out, err=self.err)
        ret = worker.start(mounts)
        # Only remember the worker if it can start (for cleanup), otherwise, an
        # error is displayed.
        self.worker = worker
        return ret

    def delete_worker(self):
        self.worker.stop()

    def run_in_container(self, command, with_creds=False):
        return self.worker.raw_shell(command, with_agent=with_creds)

    def setup_project(self, remote_work_dir):
        setup_cmd = self.worker.backing.conf.get('byoci.setup.command')
        if not setup_cmd:
            return (0, None)
        logger.info('{} setup on top of {}'.format(
            self.worker.name, self.worker.backing_name))
        logger.info('Running {}'.format(setup_cmd))
        return (self.run_in_container(['cd', remote_work_dir, '&&', setup_cmd],
                                      with_creds=True),
                setup_cmd)

    def run_tests(self, remote_work_dir):
        test_cmd = self.worker.backing.conf.get('byoci.tests.command')
        logger.info('Running {}'.format(test_cmd))
        if not test_cmd:
            return (1, '<Unset, failing.>')
        return (self.run_in_container(['cd', remote_work_dir, '&&', test_cmd]),
                test_cmd)


class RunTests(CommandWithContainer):

    name = 'run-tests'
    description = 'Run setup and tests for a branch in a worker.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'path', metavar='PATH',
            help='Path to the tested tree.')
        self.parser.add_argument(
            'container_name', metavar='CONTAINER',
            help='The base container to build the worker.')

    def run(self):
        try:
            local_work_dir = self.options.path
            mounts, remote_work_dir = self.get_mounts_and_remote(
                local_work_dir)
            logger.info('Creating worker...')
            with byoci.working_directory(local_work_dir):
                ret = self.create_worker(
                    self.options.container_name, mounts=mounts)
            if ret:
                # if self.out or self.err are not set to sys.std{out,err}, they
                # may contain useful information.
                if self.out == sys.stdout:
                    out = 'sent to stdout'
                else:
                    out = self.out.getvalue()
                    if self.err == sys.stderr:
                        err = 'sent to stderr'
                    else:
                        err = self.err.getvalue()
                msg = ('Creation failed for {} with {}:'
                       '\n\tstdout: {}\n\tstderr: {}')
                logger.error(msg.format(self.worker.name, ret, out, err))
                return ret
            logger.info('{} setup on top of {}'.format(
                self.worker.name, self.worker.backing_name))
            ret, setup_cmd = self.setup_project(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(setup_cmd))
                return ret
            ret, test_cmd = self.run_tests(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(test_cmd))
            return ret
        finally:
            if self.worker is not None:
                self.delete_worker()


command_registry.register(RunTests)


class RunInWorker(CommandWithContainer):

    name = 'run-in-worker'
    description = 'Run commands in a worker.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'container_name', metavar='CONTAINER',
            help='The base container to build the worker.')
        self.parser.add_argument(
            'commands', metavar='COMMAND', nargs='+',
            help='A command to run in the worker.'
            ' Prefix with with-credentials to allow authenticated access.')

    def run(self):
        try:
            local_work_dir = os.getcwd()
            mounts, remote_work_dir = self.get_mounts_and_remote(
                local_work_dir)
            logger.info('Creating worker...')
            with byoci.working_directory(local_work_dir):
                ret = self.create_worker(
                    self.options.container_name, mounts=mounts)
            if ret:
                # if self.out or self.err are not set to sys.std{out,err}, they
                # may contain useful information.
                if self.out == sys.stdout:
                    out = 'sent to stdout'
                else:
                    out = self.out.getvalue()
                    if self.err == sys.stderr:
                        err = 'sent to stderr'
                    else:
                        err = self.err.getvalue()
                msg = ('Creation failed for {} with {}:'
                       '\n\tstdout: {}\n\tstderr: {}')
                logger.error(msg.format(self.worker.name, ret, out, err))
                return ret
            logger.info('{} setup on top of {}'.format(
                self.worker.name, self.worker.backing_name))
            ret = 0
            creds_prefix = 'with-credentials '
            # FIXME: It would be nice to get the commands from the config,
            # byoci.commands ? {project}.commands ? {job}.commands ?
            # -- vila 2017-02-08
            for command in self.options.commands:
                if command.startswith(creds_prefix):
                    with_creds = True
                    command = command[len(creds_prefix):]
                else:
                    with_creds = False
                msg = 'Running `{}` in a {} worker'.format(
                    command, self.options.container_name)
                if with_creds:
                    msg += ' with credentials'
                logger.info(msg)
                ret = self.run_in_container(
                    ['cd', remote_work_dir, '&&', command],
                    with_creds)
                if ret:
                    logger.error('{} failed in {}'.format(command,
                                                          self.worker.name))
                    return ret
            return ret
        finally:
            if self.worker is not None:
                self.delete_worker()


command_registry.register(RunInWorker)


# FIXME: Add support for pre-requisites -- vila 2017-01-30
# FIXME: Aka: don't land if a pre-requisite has not landed. -- vila 2018-06-30
class LandApprovedProposal(CommandWithContainer):

    class Rejected(Exception):
        """The exception used when a proposal is rejected."""

        def __init__(self, reason):
            self.reason = reason

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'target', metavar='TARGET',
            help=self.target_help)
        self.parser.add_argument(
            'work_dir', metavar='WORKINGDIR',
            help='Where the target is checked out.')
        self.parser.add_argument(
            'container_name', metavar='CONTAINER',
            help='The container name where gating tests are run.')

    def vcs(self, vcs_cmd_name, args):
        try:
            vcs_cmd = [vcs_cmd_name] + args
            return subprocesses.run(vcs_cmd)
        except errors.CommandError:
            logger.exception('{} failed'.format(' '.join(vcs_cmd)))
            raise

    # FIXME: Every method with 'proposal' in its name or as a paremeter is
    # yelling: "composition !" -- vila 2017-02-06
    def get_target(self, url):
        """Get the launchpad object the proposals are targeted.

        :param url: Describing the target
        """
        raise NotImplementedError(self.get_target)

    def proposal_comment_subject(self, proposal):
        """Build a comment subject for the given proposal.

        :param proposal: The merge proposal needing a comment.
        """
        raise NotImplementedError(self.proposal_comment_subject)

    def setup_merge_target(self, target_url, work_dir):
        """Setup a branch in a specified directory.

        :param target_url: Branch url.

        :param work_dir: Path to install the branch at.
        """
        cmd = self.setup_tree_class(out=self.out, err=self.err)
        cmd.parse_args([target_url, work_dir])
        return cmd.run()

    def merge_proposed_branch(self, work_dir, proposal):
        """Merge the proposed branch into the target.

        :param work_dir: Path where the merge should occur.

        :param proposal: Launchpad proposal to merge.
        """
        raise NotImplementedError(self.merge_proposed_branch)

    def commit_proposal(self, work_dir, proposal, commit_msg=''):
        """Commit the current working tree.

        :param work_dir: Path where the commit should occur.

        :param proposal: Launchpad proposal already merged.

        :param commit_msg: The commit message to use when committing the merge.
        """
        author = self.get_author(work_dir, proposal.reviewed_revid)
        # Decorate commits (not as sexy as lp but works from the branch alone,
        # so, anywhere).
        commit_msg += '\n\nMerged from {}'.format(proposal.web_link)
        return author, commit_msg

    def push_merged_proposal(self, work_dir, target_url):
        """Push the merged proposal to its target.

        :param work_dir: Path from where the push is done.

        :param target_url: Branch url to push to.
        """
        raise NotImplementedError(self.push_merged_proposal)

    def reject_proposal(self, proposal, reason):
        subject = self.proposal_comment_subject(proposal)
        # Include a reference to the job url if running under jenkins
        content = reason
        build_url = os.environ.get('BUILD_URL', None)
        if build_url:
            content += '\n' + build_url
        proposal.createComment(subject=subject, content=content)
        proposal.setStatus(status='Needs review',
                           revid=proposal.reviewed_revid)

    def land_proposal(self, proposal, target_url):

        logger.info('Trying to land {}'.format(proposal.web_link))
        try:
            commit_msg = proposal.commit_message or proposal.description
            if not commit_msg:
                # If neither the commit message nor the cover letter is set,
                # the proposal is not ready to be reviewed
                raise self.Rejected('A commit message must be set')
            if not launchpad.is_approved(proposal, self.target):
                raise self.Rejected('Voting criteria not met')
            local_work_dir = os.path.realpath(self.options.work_dir)
            logger.info('Getting {}'.format(target_url))
            self.setup_merge_target(target_url, local_work_dir)
            logger.info('Merging {}'.format(proposal.web_link))
            try:
                # FIXME: If the approved revision is not the tip of the
                # proposed branch, refuse to land and set status back to
                # needsReview -- vila 20180-03-01
                merged = self.merge_proposed_branch(local_work_dir, proposal)
            except errors.CommandError:
                raise self.Rejected('Merging failed')
            if not merged:
                logger.error('Nothing to merge from {}'.format(
                    proposal.web_link))
                raise self.Rejected('There was nothing to merge')
            mounts, remote_work_dir = self.get_mounts_and_remote(
                local_work_dir)
            logger.info('Creating worker...')
            with byoci.working_directory(local_work_dir):
                self.create_worker(self.options.container_name, mounts=mounts)
            ret, setup_cmd = self.setup_project(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(setup_cmd))
                raise self.Rejected('Project setup failed')
            ret, test_cmd = self.run_tests(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(test_cmd))
                raise self.Rejected('Running landing tests failed')
            self.commit_proposal(local_work_dir, proposal, commit_msg)
            self.push_merged_proposal(local_work_dir, target_url)
            # FIXME: Once webhooks are used, lp can be trusted to do that (with
            # some delay), revert this once this has been verified
            # -- vila 2017-03-30
            proposal.setStatus(status='Merged')
            logger.info('{} has landed'.format(proposal.web_link))
            return 0
        except self.Rejected as e:
            logger.info('{} could not be landed: {}'.format(
                proposal.web_link, e.reason))
            self.reject_proposal(proposal, e.reason)
            return 1
        finally:
            if self.worker is not None:
                self.delete_worker()

    def run(self):
        self.lp = launchpad.Launchpad(config.VmStack(None))
        self.target = self.get_target(self.options.target)
        if self.target is None:
            logger.error(self.wrong_target.format(self.options.target))
            return 1
        logger.info('Searching proposals for {}'.format(
            self.target.web_link))
        for proposal in self.target.landing_candidates:
            logger.debug('Looking at {}'.format(proposal.web_link))
            unique_name = self.proposal_unique_name(proposal)
            if unique_name != self.target.unique_name:
                logger.debug('Ignoring, target is {}'.format(
                    unique_name))
                continue
            queue_status = proposal.queue_status
            if queue_status != 'Approved':
                logger.debug('Ignoring, status is {}'.format(queue_status))
                continue
            # The proposal is approved
            logger.info('{} is approved'.format(proposal.web_link))
            return self.land_proposal(proposal, self.options.target)
        # None of the proposals are approved. Returning an error here cause job
        # failures for little added value.
        logger.error('No proposal is approved')
        return 0


class LandApprovedBzrProposal(LandApprovedProposal):

    name = 'land-approved-bzr-proposal'
    description = 'Land an approved bzr merge proposal.'
    target_help = 'The bazaar target branch for the merge proposals.'
    wrong_target = '{} is not a bzr branch'
    setup_tree_class = SetupBzrTree

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def bzr(self, args):
        return self.vcs('bzr', args)

    def get_target(self, url):
        return self.lp.get_bzr_branch(url)

    def proposal_comment_subject(self, proposal):
        # Uses display_name (lp:xxx)
        return 'Re: [Merge] {} into {}'.format(
            proposal.source_branch.display_name,
            proposal.target_branch.display_name)

    def merge_proposed_branch(self, work_dir, proposal):
        with byoci.working_directory(work_dir):
            lp_url = proposal.source_branch.bzr_identity
            # FIXME: This is where
            # https://bugs.launchpad.net/ols-jenkaas/+bug/1663246 needs more
            # work (and the git implementation too). A possible fix is just to
            # *not* specify '-r', proposal.reviewed_revid but that means
            # ignoring what has been top-approved and as such is worth
            # discussing whether it's the right thing to do. -- vila 2017-02-09
            ret, out, err = self.bzr(
                ['merge', lp_url, '-r', proposal.reviewed_revid])
            # FIXME: Empty merges detection is brittle. The last known issue
            # was worked around in the tests by making sure BZR_PROGRESS_BAR
            # was not set. Caveat emptor. -- vila 2017-11-30
            if err == 'Nothing to do.\n':
                # There was nothing to merge
                return False
            else:
                return True

    def get_author(self, work_dir, revid):
        # FIXME: Not explicitly tested -- vila 2017-01-26
        with byoci.working_directory(work_dir):
            log = self.bzr(['log', '-l1', '-r', revid])[1]
            for line in log.splitlines():
                if line.startswith('author:'):
                    return line[len('author: '):].rstrip('\n')
                if line.startswith('committer:'):
                    return line[len('committer: '):].rstrip('\n')
            return 'unknown'

    def commit_proposal(self, work_dir, proposal, commit_msg=''):
        author, commit_msg = super().commit_proposal(
            work_dir, proposal, commit_msg)
        with byoci.working_directory(work_dir):
            self.bzr(['commit', '-m', commit_msg, '--author', author])
        return author, commit_msg

    def push_merged_proposal(self, work_dir, target_url):
        with byoci.working_directory(work_dir):
            self.bzr(['push', target_url])

    def proposal_unique_name(self, proposal):
        return proposal.target_branch.unique_name


command_registry.register(LandApprovedBzrProposal)


class LandApprovedGitProposal(LandApprovedProposal):

    name = 'land-approved-git-proposal'
    description = 'Land an approved git merge proposal.'
    target_help = 'The target git repository branch for the merge proposals.'
    wrong_target = '{} is not a git repository'
    setup_tree_class = SetupGitTree

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIXME: Shouldn't we mention the branch inside the repository there ?
        # Even if defaulting to 'master' -- vila 2016-12-07

    def git(self, args):
        return self.vcs('git', args)

    def get_target(self, url):
        return self.lp.get_git_repo(url)

    def proposal_comment_subject(self, proposal):
        # Uses unique_name (xxx)
        proposed_url = '{}:{}'.format(
            proposal.source_git_repository.unique_name,
            proposal.source_git_path[len('refs/heads/'):])
        target_url = '{}:{}'.format(
            proposal.target_git_repository.unique_name,
            proposal.target_git_path[len('refs/heads/'):])
        return 'Re: [Merge] {} into {}'.format(proposed_url, target_url)

    def merge_proposed_branch(self, work_dir, proposal):
        with byoci.working_directory(work_dir):
            self.git(['fetch', proposal.source_git_repository.git_identity,
                      proposal.source_git_path])
            ret, out, err = self.git(['merge', '--no-ff', '--no-commit',
                                      proposal.reviewed_revid])
            # FIXME: Brittle reliance on precise git output that changed
            # between 2.7.4 and 2.17.1 -- vila 2018-07-19
            if out in ('Already up-to-date.\n',  # 2.7.4
                       'Already up to date.\n'):  # 2.17.4
                # There was nothing to merge
                return False
            else:
                return True

    def get_author(self, work_dir, revid):
        with byoci.working_directory(work_dir):
            author = self.git(['log', '-1', '--format=%aN <%aE>',
                               revid])[1].rstrip('\n')
        return author

    def commit_proposal(self, work_dir, proposal, commit_msg=''):
        author, commit_msg = super().commit_proposal(
            work_dir, proposal, commit_msg)
        with byoci.working_directory(work_dir):
            self.git(['commit', '-m', commit_msg, '--author', author])
        return author, commit_msg

    def push_merged_proposal(self, work_dir, target_url, branch='master'):
        with byoci.working_directory(work_dir):
            self.git(['push', target_url, branch])

    def proposal_unique_name(self, proposal):
        return proposal.target_git_repository.unique_name


command_registry.register(LandApprovedGitProposal)


# FIXME: target really is project :-/ -- vila 2017-08-01
class LandApprovedGitlabProposal(LandApprovedProposal):

    name = 'land-approved-gitlab-proposal'
    description = 'Land an approved gitlab merge proposal.'
    target_help = 'The project[;branch] for the merge proposals.'
    wrong_target = '{} is not a gitlab branch'
    setup_tree_class = SetupGitTree

    def parse_args(self, args):
        super().parse_args(args)
        if ';' in self.options.target:
            (self.project_path,
             self.branch_name) = self.options.target.split(';')
        else:
            self.project_path = self.options.target
            self.branch_name = 'master'
        return self.options

    def run(self):
        self.gl = gitlab.Gitlab(config.VmStack(None))
        try:
            self.project = self.gl.get_project(self.project_path)
        except KeyError:
            logger.error(self.wrong_target.format(self.options.target))
            return 1
        try:
            self.gl.get_branch(self.project_path, self.branch_name)
        except KeyError:
            logger.error(self.wrong_target.format(self.options.target))
            return 1
        proposals = self.gl.get_proposals(self.project_path,
                                          self.branch_name)
        for proposal in proposals:
            logger.info('Looking at {}'.format(proposal['web_url']))
            if proposal['target_branch'] != self.branch_name:
                logger.info('Ignoring, target is {}'.format(
                    proposal['target_branch']))
                continue
            if not is_gitlab_proposal_approved(proposal):
                continue
            # The proposal is approved
            logger.info('{} is approved'.format(proposal['web_url']))
            return self.land_proposal(proposal)
        # None of the proposals are approved. Returning an error here cause job
        # failures for little added value.
        logger.error('No proposal is approved')
        return 0

    # FIXME: When refactoring land_proposal, below is the right direction
    # (target_url is already a command attribute or can be, it's something
    # around project['ssh_url_to_repo'] or proposal['web_url'])
    # -- vila 2018-07-31
    def land_proposal(self, proposal):
        logger.info('Trying to land {}'.format(proposal['web_url']))
        try:
            description = proposal['description'] or ''
            commit_msg = '{}\n\n{}'.format(proposal['title'], description)
            if not is_gitlab_proposal_approved(proposal):
                raise self.Rejected('{} is not approved'.format(
                    proposal['web_url']))
            local_work_dir = os.path.realpath(self.options.work_dir)
            logger.info('Getting {} {}'.format(self.project_path,
                                               self.branch_name))
            target_url = '{};{}'.format(self.project['ssh_url_to_repo'],
                                        proposal['target_branch'])
            self.setup_merge_target(target_url, local_work_dir)
            logger.info('Merging {}'.format(proposal['web_url']))
            try:
                # FIXME: If the approved revision is not the tip of the
                # proposed branch, refuse to land and set status back to
                # needsReview -- vila 20180-03-01
                merged = self.merge_proposed_branch(local_work_dir, proposal)
            except errors.CommandError:
                raise self.Rejected('Merging failed')
            if not merged:
                logger.error('Nothing to merge from {}'.format(
                    proposal['web_url']))
                raise self.Rejected('There was nothing to merge')
            mounts, remote_work_dir = self.get_mounts_and_remote(
                local_work_dir)
            logger.info('Creating worker...')
            with byoci.working_directory(local_work_dir):
                self.create_worker(self.options.container_name, mounts=mounts)
            ret, setup_cmd = self.setup_project(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(setup_cmd))
                raise self.Rejected('Project setup failed')
            ret, test_cmd = self.run_tests(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(test_cmd))
                raise self.Rejected('Running landing tests failed')
            self.commit_proposal(local_work_dir, proposal, commit_msg)
            self.push_merged_proposal(
                local_work_dir, self.project['ssh_url_to_repo'],
                self.branch_name)
            logger.info('{} has landed'.format(proposal['web_url']))
            return 0
        except self.Rejected as e:
            logger.info('{} could not be landed: {}'.format(
                proposal['web_url'], e.reason))
            self.reject_proposal(proposal, e.reason)
            return 1
        finally:
            if self.worker is not None:
                self.delete_worker()

    def reject_proposal(self, proposal, reason):
        subject = self.proposal_comment_subject(proposal)
        # Include a reference to the job url if running under jenkins
        content = reason
        build_url = os.environ.get('BUILD_URL', None)
        if build_url:
            content += '\n' + build_url
        self.gl.create_proposal_comment(self.project_path, proposal['iid'],
                                        subject + '\n' + content)
        self.gl.mark_proposal(self.project_path, proposal['iid'],
                              'landing-failed')

    def git(self, args):
        return self.vcs('git', args)

    def proposal_comment_subject(self, proposal):
        # gitlab doesn't expose the mail subject
        return ''

    def merge_proposed_branch(self, work_dir, proposal):
        with byoci.working_directory(work_dir):
            self.git(['fetch', self.project['ssh_url_to_repo'],
                      proposal['source_branch']])
            ret, out, err = self.git(['merge', '--no-ff', '--no-commit',
                                      proposal['sha']])
            # FIXME: Brittle reliance on precise git output that changed
            # between 2.7.4 and 2.17.1 -- vila 2018-07-19
            if out in ('Already up-to-date.\n',  # 2.7.4
                       'Already up to date.\n'):  # 2.17.4
                # There was nothing to merge
                return False
            else:
                return True

    def get_author(self, work_dir, revid):
        with byoci.working_directory(work_dir):
            author = self.git(['log', '-1', '--format=%aN <%aE>',
                               revid])[1].rstrip('\n')
        return author

    def commit_proposal(self, work_dir, proposal, commit_msg=''):
        author = self.get_author(work_dir, proposal['sha'])
        commit_msg += '\n\nMerged from {}'.format(proposal['web_url'])
        with byoci.working_directory(work_dir):
            self.git(['commit', '-m', commit_msg, '--author', author])
        return author, commit_msg

    def push_merged_proposal(self, work_dir, target_url, branch):
        with byoci.working_directory(work_dir):
            self.git(['push', target_url, branch])


command_registry.register(LandApprovedGitlabProposal)


def is_gitlab_proposal_testable(proposal):
    if 'testing' in proposal['labels']:
        logger.info('Ignoring, tests in progress')
        return False
    if 'tests-pass' in proposal['labels']:
        logger.info('Ignoring, already tested')
        return False
    if 'tests-fail' in proposal['labels']:
        logger.info('Ignoring, already tested')
        return False
    return True


# MISSINGTESTS: based on ApprovedGitlabProposals ones -- vila 2018-08-08
class TestGitlabProposal(LandApprovedProposal):

    name = 'test-gitlab-proposal'
    description = 'Test a gitlab merge proposal.'
    target_help = 'The project[;branch] for the merge proposals.'
    wrong_target = '{} is not a gitlab branch'
    setup_tree_class = SetupGitTree

    def parse_args(self, args):
        super().parse_args(args)
        if ';' in self.options.target:
            (self.project_path,
             self.branch_name) = self.options.target.split(';')
        else:
            self.project_path = self.options.target
            self.branch_name = 'master'
        return self.options

    def run(self):
        self.gl = gitlab.Gitlab(config.VmStack(None))
        try:
            self.project = self.gl.get_project(self.project_path)
        except KeyError:
            logger.error(self.wrong_target.format(self.options.target))
            return 1
        try:
            self.gl.get_branch(self.project_path, self.branch_name)
        except KeyError:
            logger.error(self.wrong_target.format(self.options.target))
            return 1
        proposals = self.gl.get_proposals(self.project_path,
                                          self.branch_name)
        for proposal in proposals:
            logger.info('Looking at {}'.format(proposal['web_url']))
            if proposal['target_branch'] != self.branch_name:
                logger.info('Ignoring, target is {}'.format(
                    proposal['target_branch']))
                continue
            if not is_gitlab_proposal_testable(proposal):
                continue
            # The proposal is testable
            logger.info('{} will be tested'.format(proposal['web_url']))
            return self.test_proposal(proposal)
        # None of the proposals are testable. Returning an error here cause job
        # failures for little added value.
        logger.error('No proposal is testable')
        return 0

    # FIXME: When refactoring land_proposal, below is the right direction
    # (target_url is already a command attribute or can be, it's something
    # around project['ssh_url_to_repo'] or proposal['web_url'])
    # -- vila 2018-07-31
    def test_proposal(self, proposal):
        logger.info('Testing {}'.format(proposal['web_url']))
        try:
            local_work_dir = os.path.realpath(self.options.work_dir)
            logger.info('Getting {} {}'.format(self.project_path,
                                               self.branch_name))
            target_url = '{};{}'.format(self.project['ssh_url_to_repo'],
                                        proposal['target_branch'])
            self.setup_merge_target(target_url, local_work_dir)
            logger.info('Merging {}'.format(proposal['web_url']))
            try:
                # FIXME: If the approved revision is not the tip of the
                # proposed branch, refuse to land and set status back to
                # needsReview -- vila 20180-03-01
                merged = self.merge_proposed_branch(local_work_dir, proposal)
            except errors.CommandError:
                raise self.Rejected('Merging failed')
            if not merged:
                logger.error('Nothing to merge from {}'.format(
                    proposal['web_url']))
                raise self.Rejected('There was nothing to merge')
            mounts, remote_work_dir = self.get_mounts_and_remote(
                local_work_dir)
            logger.info('Creating worker...')
            with byoci.working_directory(local_work_dir):
                self.create_worker(self.options.container_name, mounts=mounts)
            ret, setup_cmd = self.setup_project(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(setup_cmd))
                raise self.Rejected('Project setup failed')
            ret, test_cmd = self.run_tests(remote_work_dir)
            if ret:
                logger.error('{} failed'.format(test_cmd))
                raise self.Rejected('Running landing tests failed')
            self.gl.mark_proposal(self.project_path, proposal['iid'],
                                  'tests-pass')
            logger.info('{} has been tested'.format(proposal['web_url']))
            return 0
        except self.Rejected as e:
            logger.info('{} could not be tested: {}'.format(
                proposal['web_url'], e.reason))
            self.reject_proposal(proposal, e.reason)
            return 1
        finally:
            if self.worker is not None:
                self.delete_worker()

    def reject_proposal(self, proposal, reason):
        subject = self.proposal_comment_subject(proposal)
        # Include a reference to the job url if running under jenkins
        content = reason
        build_url = os.environ.get('BUILD_URL', None)
        if build_url:
            content += '\n' + build_url
        self.gl.create_proposal_comment(self.project_path, proposal['iid'],
                                        subject + '\n' + content)
        self.gl.mark_proposal(self.project_path, proposal['iid'],
                              'tests-fail')

    def git(self, args):
        return self.vcs('git', args)

    def proposal_comment_subject(self, proposal):
        # gitlab doesn't expose the mail subject
        return ''

    def merge_proposed_branch(self, work_dir, proposal):
        with byoci.working_directory(work_dir):
            self.git(['fetch', self.project['ssh_url_to_repo'],
                      proposal['source_branch']])
            ret, out, err = self.git(['merge', '--no-ff', '--no-commit',
                                      proposal['sha']])
            # FIXME: Brittle reliance on precise git output that changed
            # between 2.7.4 and 2.17.1 -- vila 2018-07-19
            if out in ('Already up-to-date.\n',  # 2.7.4
                       'Already up to date.\n'):  # 2.17.4
                # There was nothing to merge
                return False
            else:
                return True


command_registry.register(TestGitlabProposal)


def run(args=None, out=None, err=None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        cmd = Help()
        cmd_name = 'help'
    else:
        cmd_name = args[0]
        args = args[1:]
        try:
            cmd_class = command_registry.get(cmd_name)
            cmd = cmd_class(out=out, err=err)
        except KeyError:
            cmd = Help(out=out, err=err)
            args = [cmd_name]
    try:
        cmd.parse_args(args)
        return cmd.run()
    except Exception as e:
        logger.debug('{} failed'.format(cmd_name), exc_info=True)
        logger.error('{} failed: {!r}'.format(cmd_name, e))
        return -1
