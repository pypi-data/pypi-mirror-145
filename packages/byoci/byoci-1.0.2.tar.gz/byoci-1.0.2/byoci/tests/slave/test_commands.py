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


import io
import os
import unittest


from byot import (
    assertions,
    scenarii,
)


from byoci.slave import (
    commands,
    config,
    containers,
)
from byoci.tests.slave import fixtures


load_tests = scenarii.load_tests_with_scenarios


class TestHelpOptions(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        help_cmd = commands.Help(out=self.out, err=self.err)
        return help_cmd.parse_args(args)

    def test_defaults(self):
        ns = self.parse_args([])
        self.assertEqual([], ns.commands)

    def test_single_command(self):
        ns = self.parse_args(['run-in-worker'])
        self.assertEqual(['run-in-worker'], ns.commands)

    def test_several_commands(self):
        ns = self.parse_args(['help', 'run-in-worker', 'not-a-command'])
        self.assertEqual(['help', 'run-in-worker', 'not-a-command'],
                         ns.commands)


class TestHelp(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def assertHelp(self, expected, args=None):
        if args is None:
            args = []
        help_cmd = commands.Help(out=self.out, err=self.err)
        help_cmd.parse_args(args)
        help_cmd.run()
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.out.getvalue())

    def test_help_alone(self):
        self.assertHelp('''\
Available commands:
\tapproved-bzr-proposals: Check for approved bzr merge proposals.
\tapproved-git-proposals: Check for approved git merge proposals.
\tapproved-gitlab-proposals: Check for approved gitlab merge proposals.
\thelp: Describe byo-ci-slave commands.
\tland-approved-bzr-proposal: Land an approved bzr merge proposal.
\tland-approved-git-proposal: Land an approved git merge proposal.
\tland-approved-gitlab-proposal: Land an approved gitlab merge proposal.
\trun-in-worker: Run commands in a worker.
\trun-tests: Run setup and tests for a branch in a worker.
\tsetup-bzr-tree: Setup a brz working tree.
\tsetup-git-tree: Setup a git workingtree.
\ttest-gitlab-proposal: Test a gitlab merge proposal.
''')

    def test_help_help(self):
        self.assertHelp('''\
usage: byo-ci-slave... help [-h] [COMMAND [COMMAND ...]]

Describe byo-ci-slave commands.

positional arguments:
  COMMAND     Display help for each command (All if none is given).

optional arguments:
  -h, --help  show this help message and exit
''',
                        ['help'])


class TestSetupTreeOptions(unittest.TestCase):

    scenarios = [('bzr', dict(command_cls=commands.SetupBzrTree)),
                 ('git', dict(command_cls=commands.SetupGitTree))]

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        approved_cmd = self.command_cls(out=self.out, err=self.err)
        return approved_cmd.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_too_much(self):
        with self.assertRaises(SystemExit):
            self.parse_args(['foo', 'bar', 'baz'])

    def test_valid(self):
        ns = self.parse_args(['source', './path'])
        self.assertEqual('source', ns.source)
        self.assertEqual('./path', ns.path)


class TestSetupGitTreeOptions(unittest.TestCase):

    command_cls = commands.SetupGitTree

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        approved_cmd = self.command_cls(out=self.out, err=self.err)
        return approved_cmd.parse_args(args)

    def test_default(self):
        ns = self.parse_args(['source', './path'])
        self.assertEqual('source', ns.source)
        self.assertEqual('./path', ns.path)
        self.assertEqual('master', ns.branch)

    def test_branch(self):
        ns = self.parse_args(['source;branch', './path'])
        self.assertEqual('source', ns.source)
        self.assertEqual('./path', ns.path)
        self.assertEqual('branch', ns.branch)


# FIXME: refactor tests to support gitlab -- vila 2018-07-30
# MISSINGTESTS: git-url;branch + parametrize (lp/gitlab) -- vila 2018-07-31
class TestSetupTree(unittest.TestCase):

    scenarios = [('bzr', dict(branch_handler=fixtures.BzrBranchHandler(),
                              command_cls=commands.SetupBzrTree)),
                 ('git', dict(branch_handler=fixtures.GitRepositoryHandler(),
                              command_cls=commands.SetupGitTree))]

    def setUp(self):
        super().setUp()
        self.lp = fixtures.use_launchpad(self)
        self.branch_handler.set_identity(self)
        self.branch_handler.set_launchpad_access(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command = self.command_cls(out=self.out, err=self.err)

    def run_command(self, args):
        self.command.parse_args(args)
        return self.command.run()

    def create_remote(self):
        branch = self.branch_handler.factory('target')
        self.addCleanup(branch.delete)
        branch.create()
        branch.update('Something', 'file: foo\nfoo content\n')
        url = self.branch_handler.lp_branch_url('target')
        branch.push(url)
        return url

    def test_existing_dir(self):
        url = self.create_remote()
        os.mkdir('work')
        lp_branch = self.branch_handler.get_branch_from_lp(self.lp, url)
        self.addCleanup(lp_branch.lp_delete)
        self.run_command([url, './work'])
        self.assertTrue(os.path.exists('work/foo'))

    def test_non_existing_subdir(self):
        url = self.create_remote()
        lp_branch = self.branch_handler.get_branch_from_lp(self.lp, url)
        self.addCleanup(lp_branch.lp_delete)
        self.run_command([url, './work/subdir/dir'])
        self.assertTrue(os.path.exists('work/subdir/dir/foo'))

    def test_unknown_branch(self):
        url = self.branch_handler.lp_branch_url('i-dont-exist')
        work_dir = './work'
        with self.assertRaises(commands.errors.CommandError):
            self.run_command([url, work_dir])
        log = self.log_stream.getvalue()
        # The log provides enough context
        expected = '{} {} failed'.format(url, work_dir)
        self.assertTrue(expected in log,
                        '[{}] not found in [{}]'.format(expected, log))


class TestRunTestsOptions(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        run_tests_cmd = commands.RunTests(out=self.out, err=self.err)
        return run_tests_cmd.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_too_much(self):
        with self.assertRaises(SystemExit):
            self.parse_args(['foo', 'bar', 'baz'])

    def test_valid(self):
        ns = self.parse_args(['./path', 'container'])
        self.assertEqual('./path', ns.path)
        self.assertEqual('container', ns.container_name)


class TestRunTests(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.isolate_from_disk_for_slave(self)
        fixtures.override_logging(self)
        self.command = commands.RunTests(out=self.out, err=self.err)
        fixtures.define_uniq_container(self)
        self.conf = config.VmStack(None)
        # Silence warnings about added hosts by using log level ERROR
        ssh_opts = ('-oLogLevel=ERROR,'
                    '-oUserKnownHostsFile=/dev/null,'
                    '-oStrictHostKeyChecking=no,'
                    '-oIdentityFile={ssh.key}')
        self.conf.set('ssh.options', ssh_opts)
        self.conf.store.save()
        self.conf.store.unload()
        # Pre-build the container or errors in that part are obscure to debug
        self.container = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.addCleanup(self.container.teardown)
        self.container.setup()

    def run_command(self):
        self.command.parse_args(['.', self.container_name])
        return self.command.run()

    def test_pass(self):
        self.conf.set('byoci.setup.command', '/bin/true')
        self.conf.set('byoci.tests.command', '/bin/true')
        self.conf.store.save()
        self.conf.store.unload()
        ret = self.run_command()
        self.assertEqual(0, ret)

    def test_setup_fails(self):
        self.conf.set('byoci.setup.command', '/bin/false')
        self.conf.store.save()
        self.conf.store.unload()
        ret = self.run_command()
        # 255 says ssh sees an error... maybe some pipe is not closed properly
        # ?  This smells like a FIXME...
        self.assertEqual(255, ret)

    def test_run_tests_fails(self):
        self.conf.set('byoci.tests.command', '/bin/false')
        self.conf.store.save()
        self.conf.store.unload()
        ret = self.run_command()
        # 255 says ssh sees an error... maybe some pipe is not closed properly
        # ?  This smells like a FIXME...
        self.assertEqual(255, ret)

    def test_run_tests_undef_fails(self):
        # Not running tests is a failure ;-)
        ret = self.run_command()
        self.assertEqual(1, ret)


class TestRunInWorkerOptions(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.command = commands.RunInWorker(out=self.out, err=self.err)

    def parse_args(self, args):
        return self.command.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_no_commands(self):
        with self.assertRaises(SystemExit):
            self.parse_args(['container'])

    def test_multiple_commands(self):
        self.parse_args(['container', 'pwd', 'whoami'])
        self.assertEqual('container', self.command.options.container_name)
        self.assertEqual(['pwd', 'whoami'], self.command.options.commands)


class TestRunInWorker(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command = commands.RunInWorker(out=self.out, err=self.err)
        fixtures.define_uniq_container(self)
        conf = config.VmStack(None)
        # Silence warnings about added hosts by using log level ERROR
        ssh_opts = ('-oLogLevel=ERROR,'
                    '-oUserKnownHostsFile=/dev/null,'
                    '-oStrictHostKeyChecking=no,'
                    '-oIdentityFile={ssh.key}')
        conf.set('ssh.options', ssh_opts)
        conf.store.save()
        conf.store.unload()
        # Pre-build the container or errors in that part are obscure to debug
        self.container = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.addCleanup(self.container.teardown)
        self.container.setup()

    def run_command(self, args):
        self.command.parse_args([self.container_name] + args)
        ret = self.command.run()
        msg = 'Run in worker {} failed with {}:\n\tstdout: {}\n\tstderr: {}'
        self.assertEqual(0, ret, msg.format(
            self.container_name, ret, self.out.getvalue(),
            self.err.getvalue()))
        return ret

    def test_create_worker_fails(self):
        # Sabotage worker
        worker_name = 'worker-{}-{}'.format(self.container_name, os.getpid())
        conf = config.VmStack(worker_name)
        conf.set('vm.packages', 'i-dont-exist')
        conf.store.save()
        conf.store.unload()
        with self.assertRaises(AssertionError):
            self.run_command(['/bin/true'])

    def test_outside_workspace(self):
        os.chdir('..')
        # FIXME: The mounts assume we're below workspace, the end result is
        # broken -- vila 2017-02-06
        self.run_command(['pwd'])
        # '/' below is '/workspace/..' a place where no access is granted
        self.assertEqual('/\n', self.out.getvalue())

    def test_inside_workspace(self):
        os.mkdir('work')
        os.chdir('work')
        self.run_command(['pwd'])
        self.assertEqual('/workspace/work\n', self.out.getvalue())

    def test_below_workspace(self):
        os.makedirs('work/dir/subdir')
        os.chdir('work/dir/subdir')
        self.run_command(['pwd'])
        self.assertEqual('/workspace/work/dir/subdir\n', self.out.getvalue())


class TestLandProposalsOptions(unittest.TestCase):

    # FIXME: Add gitlab (command & scenario).
    scenarios = [('bzr', dict(command_cls=commands.LandApprovedBzrProposal)),
                 ('git', dict(command_cls=commands.LandApprovedGitProposal))]

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.command = self.command_cls(out=self.out, err=self.err)

    def parse_args(self, args):
        return self.command.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_mandatory_args(self):
        self.parse_args(['target', 'work', 'container'])
        self.assertEqual('target', self.command.options.target)
        self.assertEqual('work', self.command.options.work_dir)
        self.assertEqual('container', self.command.options.container_name)


class TestApprovalCommands(unittest.TestCase):
    """Base class for launchpad approval landing commands related tests.

    This setup the scenarios and the common fixtures.
    """

    scenarios = [('bzr', dict(branch_handler=fixtures.BzrBranchHandler(),
                              proposal_handler=fixtures.BzrProposalHandler(),
                              command_cls=commands.LandApprovedBzrProposal)),
                 ('git', dict(branch_handler=fixtures.GitRepositoryHandler(),
                              proposal_handler=fixtures.GitProposalHandler(),
                              command_cls=commands.LandApprovedGitProposal))]

    def setUp(self):
        super().setUp()
        self.lp = fixtures.use_launchpad(self)
        self.branch_handler.set_identity(self)
        self.branch_handler.set_launchpad_access(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command = self.command_cls(out=self.out, err=self.err)

    def Container(self):
        c = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.assertEqual('UNKNOWN', c.status())
        return c

    def run_command(self, args):
        self.command.parse_args(args)
        return self.command.run()


# FIXME: Add gitlab (command scenario).
class TestApprovedProposalsErrors(TestApprovalCommands):
    """Test the error scenarios for the land-approved-*-proposals commands."""

    def setUp(self):
        super().setUp()
        fixtures.setup_proposal_target(self)
        # Fake running under jenkins so comments on failure can be checked
        self.fake_url = 'http://jenkins.fake/job/x/42'
        fixtures.override_env(self, 'BUILD_URL', self.fake_url)

    def assertLogEndsWith(self, expected):
        log = self.log_stream.getvalue()
        self.assertTrue(log.endswith(expected), log)

    def run_command(self, args):
        # For the tests in this class only the target url is needed so fake the
        # other mandatory command args
        dummy_args = ['./work', 'container']
        self.command.parse_args(args + dummy_args)
        return self.command.run()

    def test_unknown_branch(self):
        unknown_url = self.branch_handler.lp_branch_url('i-dont-exist')
        ret = self.run_command([unknown_url])
        self.assertEqual(1, ret)
        self.assertEqual(self.command.wrong_target.format(unknown_url) + '\n',
                         self.log_stream.getvalue())

    def test_no_proposals(self):
        ret = self.run_command([self.target_url])
        self.assertEqual(0, ret)
        self.assertLogEndsWith('No proposal is approved\n')

    def test_not_approved(self):
        fixtures.create_proposal(self, 'not-approved')
        ret = self.run_command([self.target_url])
        self.assertEqual(0, ret)
        self.assertLogEndsWith('No proposal is approved\n')

    def test_no_commit_message_nor_cover_letter(self):
        proposal = fixtures.create_proposal(self, 'approved', approved=True,
                                            commit_msg='')
        ret = self.run_command([self.target_url])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            '{} could not be landed: A commit message must be set\n'.format(
                proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Needs review', proposal.queue_status)
        last_comment = list(proposal.all_comments)[-1]
        self.assertEqual(
            'A commit message must be set\n{}'.format(self.fake_url),
            last_comment.message_body)

    def test_needs_fixing(self):
        proposal = fixtures.create_proposal(self, 'approved', approved=True)
        proposal.createComment(subject='subject2', vote='Needs Fixing',
                               content='there is an issue')
        ret = self.run_command([self.target_url])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            '{} could not be landed: Voting criteria not met\n'.format(
                proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Needs review', proposal.queue_status)
        last_comment = list(proposal.all_comments)[-1]
        self.assertEqual(
            'Voting criteria not met\n{}'.format(self.fake_url),
            last_comment.message_body)


class TestMergeProposedBranch(TestApprovalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_proposal_target(self)
        # Create the proposal
        self.proposal = fixtures.create_proposal(
            self, 'proposed', approved=True)
        self.work_dir = './work'
        # Prepare the proposal merge
        self.command.setup_merge_target(self.target_url, self.work_dir)

    def test_merge_succeeds(self):
        self.command.merge_proposed_branch(self.work_dir, self.proposal)
        self.assertTrue(os.path.exists('work/proposed'))

    def test_already_merged(self):
        # Until webhooks are used, the current design may trigger an attempt to
        # land the same proposal twice.
        self.command.merge_proposed_branch(self.work_dir, self.proposal)
        self.command.commit_proposal(self.work_dir, self.proposal)
        self.assertFalse(self.command.merge_proposed_branch(
            self.work_dir, self.proposal))

    def test_merge_conflicts(self):
        # Inject a conflicting revision in the work branch
        target = self.branch_handler.factory('work')
        target.update('new content for proposed',
                      'file: proposed\nnew content\n')
        with self.assertRaises(commands.errors.CommandError):
            self.command.merge_proposed_branch(self.work_dir, self.proposal)
        # The log provides enough context
        log = self.log_stream.getvalue()
        expected = 'merge'
        self.assertTrue(expected in log,
                        '[{}] not found in [{}]'.format(expected, log))


class TestCommitProposal(TestApprovalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_proposal_target(self)
        # Create the proposal
        self.proposal = fixtures.create_proposal(
            self, 'proposed', approved=True,
            # Use a unicode commit message to exercise code paths from local
            # host to launchpad and back as well as vcs commands.
            commit_msg='Unbreakable\xa0Unicode\xa0Space')
        self.work_dir = './work'
        # Merge the proposal
        self.command.setup_merge_target(self.target_url, self.work_dir)
        self.command.merge_proposed_branch(self.work_dir, self.proposal)

    def test_commit_succeeds(self):
        self.command.commit_proposal(self.work_dir, self.proposal)
        # FIXME: Check log ? -- vila 2017-01-24

# MISSINGTEST: What if the commit fails ? Enough feedback ?


class TestPushMergedProposal(TestApprovalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_proposal_target(self)
        # Create the proposal
        self.proposal = fixtures.create_proposal(
            self, 'proposed', approved=True)
        self.work_dir = './work'
        # Merge the proposal and commit
        self.command.setup_merge_target(self.target_url, self.work_dir)
        self.command.merge_proposed_branch(self.work_dir, self.proposal)
        self.command.commit_proposal(self.work_dir, self.proposal)

    def test_push_succeeds(self):
        self.command.push_merged_proposal(self.work_dir, self.target_url)
        # FIXME: Check log ? -- vila 2017-01-24

# MISSINGTEST: What if the push fails ? Enough feedback ?


class TestCommandWithContainer(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command = commands.CommandWithContainer(
            out=self.out, err=self.err)
        fixtures.define_uniq_container(self)
        conf = config.VmStack(None)
        # Silence warnings about added hosts by using log level ERROR
        ssh_opts = ('-oLogLevel=ERROR,'
                    '-oUserKnownHostsFile=/dev/null,'
                    '-oStrictHostKeyChecking=no,'
                    '-oIdentityFile={ssh.key}')
        conf.set('ssh.options', ssh_opts)
        conf.store.save()
        conf.store.unload()
        self.base_container = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.addCleanup(self.base_container.teardown)
        ret = self.command.create_worker(
            self.container_name, name='worker-' + self.container_name)
        self.addCleanup(self.command.delete_worker)
        self.assertEqual(
            0, ret,
            'Create worker {} failed with {}:\n'
            '\tstdout: {}\n\tstderr: {}\n'.format(
                'worker-' + self.container_name, ret,
                self.out.getvalue(), self.err.getvalue()))
        self.assertEqual(0, ret)

    def test_command_success(self):
        ret = self.command.run_in_container(['/bin/true'])
        self.assertEqual(0, ret)
        self.assertEqual('', self.out.getvalue())
        self.assertEqual('', self.err.getvalue())

    def test_command_fails(self):
        ret = self.command.run_in_container(['/bin/false'])
        # 255 says ssh sees an error... maybe some pipe is not closed properly
        # ?  This smells like a FIXME...
        self.assertEqual(255, ret)
        self.assertEqual('', self.out.getvalue())
        # self.assertEqual('', self.err.getvalue())

    def test_command_output(self):
        ret = self.command.run_in_container(['whoami'])
        self.assertEqual(0, ret)
        # This got captured by the command.out stream
        self.assertEqual('ubuntu\n', self.out.getvalue())
        self.assertEqual('', self.err.getvalue())

    def test_with_creds(self):
        ret = self.command.run_in_container(['ssh-add', '-l'], with_creds=True)
        self.assertEqual(0, ret)
        # Check that the right key and only that key is provided by the agent.
        ssh_key = self.command.worker.conf.get('ssh.key')
        lines = self.out.getvalue().splitlines()
        assertions.assertLength(self, 1, lines)
        self.assertTrue(ssh_key in lines[0])
        self.assertEqual('', self.err.getvalue())

    def test_without_creds(self):
        ret = self.command.run_in_container(['ssh-add', '-l'],
                                            with_creds=False)
        # 255 (instead of 2) says ssh sees an error... maybe some pipe is not
        # closed properly ?  This smells like a FIXME...
        self.assertEqual(255, ret)
        self.assertEqual('', self.out.getvalue())
        err_msg = self.err.getvalue()
        # because we tunnel through ssh, we get more \n...
        self.assertTrue(
            err_msg.endswith(
                'Could not open a connection to your authentication agent.'
                '\n\n\n'),
            err_msg)


class TestSetupVcs(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command = commands.CommandWithContainer(
            out=self.out, err=self.err)
        fixtures.define_uniq_container(self)
        conf = config.VmStack(None)
        # Silence warnings about added hosts by using log level ERROR
        ssh_opts = ('-oLogLevel=ERROR,'
                    '-oUserKnownHostsFile=/dev/null,'
                    '-oStrictHostKeyChecking=no,'
                    '-oIdentityFile={ssh.key}')
        conf.set('ssh.options', ssh_opts)

    def setup_worker(self, vm_packages):
        conf = config.VmStack(self.container_name)
        conf.set('vm.packages', vm_packages)
        if vm_packages:
            # Some packages may fail to install without an update
            conf.set('vm.update', 'True')
        conf.store.save()
        conf.store.unload()
        self.base_container = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.addCleanup(self.base_container.teardown)
        ret = self.command.create_worker(self.container_name,
                                         name='worker-' + self.container_name)
        self.addCleanup(self.command.delete_worker)
        self.assertEqual(0, ret)

    def test_config_files_present(self):
        self.setup_worker('bzr')
        ret = self.command.run_in_container(['ls ~/.bazaar/bazaar.conf'])
        self.assertEqual(0, ret)
        # git seems to be installed on lxd images so it's always there
        ret = self.command.run_in_container(['ls', '~/.gitconfig'])
        self.assertEqual(0, ret)

    def test_config_files_absent(self):
        self.setup_worker('')
        ret = self.command.run_in_container(['ls ~/.bazaar/bazaar.conf'])
        # 255 (instead of 2) says ssh sees an error... maybe some pipe is not
        # closed properly ?  This smells like a FIXME...
        self.assertEqual(255, ret)
        # git seems to be installed on lxd images so it's always there
        ret = self.command.run_in_container(['ls', '~/.gitconfig'])
        self.assertEqual(0, ret)


class TestLandings(TestApprovalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_proposal_target(self)
        fixtures.define_uniq_container(self)
        # Fake running under jenkins so comments on failure can be checked
        self.fake_url = 'http://jenkins.fake/job/x/42'
        fixtures.override_env(self, 'BUILD_URL', self.fake_url)

    def assertLandingSucceeds(self, ret):
        msg = ('Landing {} failed with {}:\n\tstdout: {}\n\tstderr: {}\n'
               '\tlog: {}')
        self.assertEqual(0, ret, msg.format(
            self.target_url, ret, self.out.getvalue(), self.err.getvalue(),
            self.log_stream.getvalue()))

    def assertLogEndsWith(self, expected):
        log = self.log_stream.getvalue()
        self.assertTrue(log.endswith(expected), log)

    def test_landing_succeeds(self):
        proposal = fixtures.create_proposal(self, 'approved', approved=True)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertLandingSucceeds(ret)
        self.assertLogEndsWith('{} has landed\n'.format(proposal.web_link))
        proposal.lp_refresh()
        # FIXME: Restore the following when webhooks are used and launchpad
        # trusted to mark the MP as merged (and decorate commits)
        # -- vila 2017-03-30
        self.assertEqual('Merged', proposal.queue_status)

    def test_cover_no_commit(self):
        proposal = fixtures.create_proposal(
            self, 'approved', approved=True, commit_msg='',
            cover='summary\n\nLong explanation')
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertLandingSucceeds(ret)
        self.assertLogEndsWith('{} has landed\n'.format(proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Merged', proposal.queue_status)
        # FIXME: Check the commit message for the merge, it should start with
        # the cover letter -- vila 2018-02-27

    def test_commit_over_cover(self):
        proposal = fixtures.create_proposal(
            self, 'approved', approved=True, commit_msg='One line comment',
            cover='summary\n\nLong explanation')
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertLandingSucceeds(ret)
        self.assertLogEndsWith('{} has landed\n'.format(proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Merged', proposal.queue_status)
        # FIXME: Check the commit message for the merge, it should start with
        # the commit msg -- vila 2018-02-27

    def test_landing_twice_fails(self):
        proposal = fixtures.create_proposal(self, 'approved', approved=True)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertEqual(
            0, ret,
            'First landing failed with {}:\n\tstdout: {}\n\tstderr: {}'.format(
                ret, self.out.getvalue(), self.err.getvalue()))
        self.assertLogEndsWith('{} has landed\n'.format(proposal.web_link))
        # Mark the MP as approved again as it has been marked as Merged.
        proposal.lp_refresh()
        proposal.setStatus(status='Approved', revid=proposal.reviewed_revid)
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            '{} could not be landed: There was nothing to merge\n'.format(
                proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Needs review', proposal.queue_status)

    def test_landing_setup_fails(self):
        proposal = fixtures.create_proposal(self, 'approved', approved=True)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/false')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            '{} could not be landed: Project setup failed\n'.format(
                proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Needs review', proposal.queue_status)
        last_comment = list(proposal.all_comments)[-1]
        self.assertEqual('Project setup failed\n{}'.format(self.fake_url),
                         last_comment.message_body)

    def test_landing_tests_fails(self):
        proposal = fixtures.create_proposal(self, 'approved', approved=True)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/false')
        self.addCleanup(base_container.teardown)
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            '{} could not be landed: Running landing tests failed\n'.format(
                proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Needs review', proposal.queue_status)
        last_comment = list(proposal.all_comments)[-1]
        self.assertEqual(
            'Running landing tests failed\n{}'.format(
                self.fake_url),
            last_comment.message_body)

    def test_landing_conflicts_fails(self):
        proposal = fixtures.create_proposal(self, 'approved', approved=True)
        # Make a conflicting change in the target
        target = self.branch_handler.factory('target')
        target.update('new content for approved',
                      'file: approved\nnew content\n')
        target.push(self.target_url)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        ret = self.run_command(
            [self.target_url, './work', self.container_name])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            '{} could not be landed: Merging failed\n'.format(
                proposal.web_link))
        proposal.lp_refresh()
        self.assertEqual('Needs review', proposal.queue_status)
        last_comment = list(proposal.all_comments)[-1]
        self.assertEqual('Merging failed\n{}'.format(self.fake_url),
                         last_comment.message_body)


# MISSINGTESTS: For ApprovedGitProposals and ApprovedBzrProposals (whose names
# should probably include launchpad for clarity -- vila 2018-07-31
class TestApprovedGitlabProposals(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.use_gitlab(self)
        self.branch_handler = fixtures.GitlabBranchHandler()
        self.branch_handler.set_identity(self)
        self.branch_handler.set_gitlab_access(self)
        fixtures.setup_gitlab_proposal_target(self)
        self.project_name = self.branch_handler.get_project_name()
        self.proposal_handler = fixtures.GitlabProposalHandler()
        self.proposal = fixtures.create_gitlab_proposal(self, 'testing')
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command_cls = commands.ApprovedGitlabProposals
        self.command = self.command_cls(out=self.out, err=self.err)

    def run_command(self):
        # For the tests in this class only the target project and branch are
        # needed
        self.command.parse_args(['{};{}'.format(self.project_name,
                                                self.target_branch_name)])
        return self.command.run()

    def assertLogEndsWith(self, expected):
        log = self.log_stream.getvalue()
        self.assertTrue(log.endswith(expected), log)

    def test_not_approved(self):
        ret = self.run_command()
        self.assertEqual(1, ret)
        self.assertLogEndsWith('No proposal is approved\n')

    def test_approved_not_tested(self):
        self.gl_reviewer.create_proposal_comment(
            self.project_name, self.proposal['iid'], 'Good stuff\n/award :+1:')
        ret = self.run_command()
        self.assertEqual(1, ret)
        self.assertLogEndsWith('No proposal is approved\n')

    def test_tested_not_approved(self):
        self.gl_dev.mark_proposal(self.project_name, self.proposal['iid'],
                                  'tests-pass')
        ret = self.run_command()
        self.assertEqual(1, ret)
        self.assertLogEndsWith('No proposal is approved\n')

    def test_tested_and_disapproved(self):
        self.gl_dev.mark_proposal(self.project_name, self.proposal['iid'],
                                  'tests-pass')
        self.gl_reviewer.create_proposal_comment(
            self.project_name,
            self.proposal['iid'],
            'Needs fixing\n/award :-1:')
        ret = self.run_command()
        self.assertEqual(1, ret)
        self.assertLogEndsWith('No proposal is approved\n')

    def test_tested_and_approved(self):
        self.gl_dev.mark_proposal(self.project_name, self.proposal['iid'],
                                  'tests-pass')
        self.gl_reviewer.create_proposal_comment(
            self.project_name, self.proposal['iid'], 'Good stuff\n/award :+1:')
        ret = self.run_command()
        self.assertEqual(0, ret)
        self.assertLogEndsWith(
            '{} is approved\n'.format(self.proposal['web_url']))


# FIXME: Unify with TestApprovalCommands
class TestLandGitlabApprovedProposalCommands(unittest.TestCase):
    """Base class for gitlab approval landing commands related tests.

    This setup the common fixtures.
    """
    branch_handler = fixtures.GitlabBranchHandler()
    proposal_handler = fixtures.GitlabProposalHandler()
    command_cls = commands.LandApprovedGitlabProposal

    def setUp(self):
        super().setUp()
        fixtures.use_gitlab(self)
        self.branch_handler.set_identity(self)
        self.branch_handler.set_gitlab_access(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command = self.command_cls(out=self.out, err=self.err)

    def Container(self):
        c = containers.Container(
            self.container_name, out=self.out, err=self.err)
        self.assertEqual('UNKNOWN', c.status())
        return c

    def run_command(self, args):
        self.command.parse_args(args)
        return self.command.run()


class TestLandGlApprovedProposalErrors(TestLandGitlabApprovedProposalCommands):
    """Test errors for the land-gitlab-approved-*-proposal commands."""

    def setUp(self):
        super().setUp()
        fixtures.setup_gitlab_proposal_target(self)
        # Fake running under jenkins so comments on failure can be checked
        self.fake_url = 'http://jenkins.fake/job/x/42'
        fixtures.override_env(self, 'BUILD_URL', self.fake_url)

    def assertLogEndsWith(self, expected):
        log = self.log_stream.getvalue()
        self.assertTrue(log.endswith(expected), log)

    def get_target_arg(self, branch=None):
        if branch is None:
            branch = self.target_branch_name
        return '{};{}'.format(self.target_project_name, branch)

    def run_command(self, args):
        # For the tests in this class only the target url is needed so fake the
        # other mandatory command args
        dummy_args = ['./work', 'container']
        self.command.parse_args(args + dummy_args)
        return self.command.run()

    def test_unknown_project(self):
        ret = self.run_command(['i-dont-exist'])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            self.command.wrong_target.format('i-dont-exist') + '\n')

    def test_unknown_branch(self):
        unknown_branch = self.get_target_arg('i-dont-exist')
        ret = self.run_command([unknown_branch])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            self.command.wrong_target.format(unknown_branch) + '\n')

    def test_no_proposals(self):
        ret = self.run_command([self.get_target_arg()])
        self.assertEqual(0, ret)
        self.assertLogEndsWith('No proposal is approved\n')

    def test_not_approved(self):
        fixtures.create_gitlab_proposal(self, 'not-approved')
        ret = self.run_command([self.get_target_arg()])
        self.assertEqual(0, ret)
        self.assertLogEndsWith('No proposal is approved\n')


class TestGitlabMergeProposedBranch(TestLandGitlabApprovedProposalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_gitlab_proposal_target(self)
        # Create the proposal
        self.proposal = fixtures.create_gitlab_proposal(
            self, 'proposed', approved=True)
        self.work_dir = './work'
        # Prepare the proposal merge
        self.command.project = self.target_project
        target_url = '{};{}'.format(self.target_project['ssh_url_to_repo'],
                                    self.proposal['target_branch'])
        self.command.setup_merge_target(target_url, self.work_dir)

    def test_merge_succeeds(self):
        self.command.merge_proposed_branch(self.work_dir, self.proposal)
        self.assertTrue(os.path.exists('work/proposed'))

    def test_already_merged(self):
        # Until webhooks are used, the current design may trigger an attempt to
        # land the same proposal twice.
        self.command.merge_proposed_branch(self.work_dir, self.proposal)
        self.command.commit_proposal(self.work_dir, self.proposal)
        self.assertFalse(self.command.merge_proposed_branch(
            self.work_dir, self.proposal))

    def test_merge_conflicts(self):
        # Inject a conflicting revision in the work branch
        target = self.branch_handler.factory('work')
        target.update('new content for proposed',
                      'file: proposed\nnew content\n')
        with self.assertRaises(commands.errors.CommandError):
            self.command.merge_proposed_branch(self.work_dir, self.proposal)
        # The log provides enough context
        log = self.log_stream.getvalue()
        expected = 'merge'
        self.assertTrue(expected in log,
                        '[{}] not found in [{}]'.format(expected, log))


class TestCommitGitlabProposal(TestLandGitlabApprovedProposalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_gitlab_proposal_target(self)
        # Create the proposal
        self.proposal = fixtures.create_gitlab_proposal(
            self, 'proposed', approved=True)
        self.work_dir = './work'
        # Prepare the proposal merge
        self.command.project = self.target_project
        target_url = '{};{}'.format(self.target_project['ssh_url_to_repo'],
                                    self.proposal['target_branch'])
        self.command.setup_merge_target(target_url, self.work_dir)
        self.command.merge_proposed_branch(self.work_dir, self.proposal)

    def test_commit_succeeds(self):
        self.command.commit_proposal(self.work_dir, self.proposal)
        # FIXME: Check log ? -- vila 2017-01-24

# MISSINGTEST: What if the commit fails ? Enough feedback ?


class TestPushGitlabMergedProposal(TestLandGitlabApprovedProposalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_gitlab_proposal_target(self)
        # Create the proposal
        self.proposal = fixtures.create_gitlab_proposal(
            self, 'proposed', approved=True)
        self.work_dir = './work'
        # Prepare the proposal merge
        self.command.project = self.target_project
        target_url = '{};{}'.format(
            self.target_project['ssh_url_to_repo'],
            self.proposal['target_branch'])
        self.command.setup_merge_target(target_url, self.work_dir)
        self.command.merge_proposed_branch(self.work_dir, self.proposal)
        self.command.commit_proposal(self.work_dir, self.proposal)

    def test_push_succeeds(self):
        self.command.push_merged_proposal(
            self.work_dir, self.command.project['ssh_url_to_repo'],
            self.target_branch_name)
        # FIXME: Check log ? -- vila 2017-01-24

# MISSINGTEST: What if the push fails ? Enough feedback ?


class TestGitlabLandings(TestLandGitlabApprovedProposalCommands):

    def setUp(self):
        super().setUp()
        fixtures.setup_gitlab_proposal_target(self)
        fixtures.define_uniq_container(self)
        # Fake running under jenkins so comments on failure can be checked
        self.fake_url = 'http://jenkins.fake/job/x/42'
        fixtures.override_env(self, 'BUILD_URL', self.fake_url)
        # Disable part of urllib3 logging, it's causing spurious msgs under
        # load
        from byoci.slave import gitlab
        gitlab.requests.packages.urllib3.connectionpool.log.propagate = False

    def assertLandingSucceeds(self, ret):
        msg = ('Landing {} failed with {}:\n\tstdout: {}\n\tstderr: {}\n'
               '\tlog: {}')
        self.assertEqual(0, ret, msg.format(
            self.target_url, ret, self.out.getvalue(), self.err.getvalue(),
            self.log_stream.getvalue()))

    def assertLogEndsWith(self, expected):
        log = self.log_stream.getvalue()
        self.assertTrue(log.endswith(expected),
                        '{} not found in {}'.format(expected, log))

    def test_landing_succeeds(self):
        proposal = fixtures.create_gitlab_proposal(
            self, 'approved', approved=True)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        target_url = '{};{}'.format(self.target_project_name,
                                    proposal['target_branch'])
        ret = self.run_command(
            [target_url, './work', self.container_name])
        self.assertLandingSucceeds(ret)
        self.assertLogEndsWith('{} has landed\n'.format(proposal['web_url']))
        updated = self.gl_dev.get_proposal(self.target_project_name,
                                           proposal['iid'])
        self.assertEqual('merged', updated['state'])

    def test_cover_no_commit(self):
        proposal = fixtures.create_gitlab_proposal(
            self, 'approved', approved=True, commit_msg='',
            cover='summary\n\nLong explanation')
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        target_url = '{};{}'.format(self.target_project_name,
                                    proposal['target_branch'])
        ret = self.run_command(
            [target_url, './work', self.container_name])
        self.assertLandingSucceeds(ret)
        self.assertLogEndsWith('{} has landed\n'.format(proposal['web_url']))
        updated = self.gl_dev.get_proposal(self.target_project_name,
                                           proposal['iid'])
        self.assertEqual('merged', updated['state'])
        # FIXME: Check the commit message for the merge, it should start with
        # the cover letter -- vila 2018-08-01

    def test_commit_over_cover(self):
        proposal = fixtures.create_gitlab_proposal(
            self, 'approved', approved=True, commit_msg='One line comment',
            cover='summary\n\nLong explanation')
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        target_url = '{};{}'.format(self.target_project_name,
                                    proposal['target_branch'])
        ret = self.run_command(
            [target_url, './work', self.container_name])
        self.assertLandingSucceeds(ret)
        self.assertLogEndsWith('{} has landed\n'.format(proposal['web_url']))
        updated = self.gl_dev.get_proposal(self.target_project_name,
                                           proposal['iid'])
        self.assertEqual('merged', updated['state'])
        # Unlike launchpad where a description and a commit message can be
        # specified on the proposal, gitlab mandates a title and leave the
        # description optional. Merging from the UI allows a commit message to
        # be specified but this message is not part of the proposal object.  So
        # on gitlab  the description is used as the commit message.

    def test_landing_twice_fails(self):
        # There doesn't seem to be a way to re-open a merged proposal so this
        # tests makes no sense on gitlab.
        pass

    def test_landing_setup_fails(self):
        proposal = fixtures.create_gitlab_proposal(
            self, 'approved', approved=True)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/false')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        self.addCleanup(base_container.teardown)
        target_url = '{};{}'.format(self.target_project_name,
                                    proposal['target_branch'])
        ret = self.run_command(
            [target_url, './work', self.container_name])
        self.assertEqual(1, ret)
        # This can break under load because of `requests` logging.
        self.assertLogEndsWith(
            '{} could not be landed: Project setup failed\n'.format(
                proposal['web_url']))
        updated = self.gl_dev.get_proposal(self.target_project_name,
                                           proposal['iid'])
        self.assertEqual('opened', updated['state'])
        feedback_comment = self.gl_dev.get_proposal_comments(
            self.target_project_name, proposal['iid'])[0]
        self.assertEqual('\nProject setup failed\n{}'.format(self.fake_url),
                         feedback_comment['body'])

    def test_landing_tests_fails(self):
        proposal = fixtures.create_gitlab_proposal(
            self, 'approved', approved=True)
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/false')
        self.addCleanup(base_container.teardown)
        target_url = '{};{}'.format(self.target_project_name,
                                    proposal['target_branch'])
        ret = self.run_command(
            [target_url, './work', self.container_name])
        self.assertEqual(1, ret)
        # This can break under load because of `requests` logging.
        self.assertLogEndsWith(
            '{} could not be landed: Running landing tests failed\n'.format(
                proposal['web_url']))
        updated = self.gl_dev.get_proposal(self.target_project_name,
                                           proposal['iid'])
        self.assertEqual('opened', updated['state'])
        feedback_comment = self.gl_dev.get_proposal_comments(
            self.target_project_name, proposal['iid'])[0]
        self.assertEqual(
            '\nRunning landing tests failed\n{}'.format(
                self.fake_url),
            feedback_comment['body'])

    def test_landing_conflicts_fails(self):
        proposal = fixtures.create_gitlab_proposal(
            self, 'approved', approved=True)
        # Make a conflicting change in the target
        target = self.branch_handler.factory('target')
        target.update('new content for approved',
                      'file: approved\nnew content\n')
        target.push(self.target_url, proposal['target_branch'])
        base_container = self.Container()
        base_container.conf.set('byoci.setup.command', '/bin/true')
        base_container.conf.set('byoci.tests.command', '/bin/true')
        target_url = '{};{}'.format(self.target_project_name,
                                    proposal['target_branch'])
        ret = self.run_command(
            [target_url, './work', self.container_name])
        self.assertEqual(1, ret)
        self.assertLogEndsWith(
            '{} could not be landed: Merging failed\n'.format(
                proposal['web_url']))
        updated = self.gl_dev.get_proposal(self.target_project_name,
                                           proposal['iid'])
        self.assertEqual('opened', updated['state'])
        feedback_comment = self.gl_dev.get_proposal_comments(
            self.target_project_name, proposal['iid'])[0]
        self.assertEqual('\nMerging failed\n{}'.format(self.fake_url),
                         feedback_comment['body'])
