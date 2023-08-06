# This file is part of Build Your Own CI
#
# Copyright 2017, 2018 Vincent Ladeuil
# Copyright 2017 Canonical Ltd.
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

from __future__ import unicode_literals

import unittest


from byot import scenarii


from byoci.slave import launchpad
from byoci.tests.slave import fixtures


load_tests = scenarii.load_tests_with_scenarios


class TestLaunchpadProposals(unittest.TestCase):

    scenarios = [('bzr', dict(branch_handler=fixtures.BzrBranchHandler(),
                              proposal_handler=fixtures.BzrProposalHandler())),
                 ('git', dict(branch_handler=fixtures.GitRepositoryHandler(),
                              proposal_handler=fixtures.GitProposalHandler()))]

    def setUp(self):
        super().setUp()
        self.lp = fixtures.use_launchpad(self)
        self.branch_handler.set_identity(self)
        self.branch_handler.set_launchpad_access(self)
        fixtures.setup_proposal_target(self)

    def test_no_mps(self):
        self.assertEqual([], list(self.target_lp_branch.landing_candidates))

    def test_create_simple_mp(self):
        proposal = fixtures.create_proposal(self, 'proposal-1')
        self.assertEqual('Needs review', proposal.queue_status)


class TestLaunchpadVotes(unittest.TestCase):

    scenarios = [('bzr', dict(branch_handler=fixtures.BzrBranchHandler(),
                              proposal_handler=fixtures.BzrProposalHandler())),
                 ('git', dict(branch_handler=fixtures.GitRepositoryHandler(),
                              proposal_handler=fixtures.GitProposalHandler()))]

    def setUp(self):
        super().setUp()
        self.lp = fixtures.use_launchpad(self)
        self.branch_handler.set_identity(self)
        self.branch_handler.set_launchpad_access(self)
        fixtures.setup_proposal_target(self)
        self.proposal = fixtures.create_proposal(self, 'wip')

    def assertApproved(self):
        approved = launchpad.is_approved(self.proposal, self.target_lp_branch)
        self.assertTrue(approved)

    def assertNotApproved(self):
        approved = launchpad.is_approved(self.proposal, self.target_lp_branch)
        self.assertFalse(approved)

    def test_no_votes(self):
        # No vote means the proposal is not approved
        self.assertNotApproved()

    def test_last_vote_wins(self):
        # Only the last vote is taken into account
        self.proposal.createComment(subject='subject1', vote='Approve',
                                    content='content1')
        self.assertApproved()
        self.proposal.createComment(subject='subject2', vote='Needs Fixing',
                                    content='content1')
        self.assertNotApproved()

    def test_outsider_vote(self):
        self.skipTest('impersonating a project outsider on launchpad'
                      ' is not implemented')
        # Fake an outsider vote

        # outsiders can't approve
        pass

    def test_pending_vote(self):
        # A pending vote blocks proposal approval
        # FIXME: A better test would be to add a review request for another
        # user -- vila 2017-01-26
        self.assertNotApproved()

    def test_approve_vote(self):
        # One authorized approved vote approves the proposal
        self.proposal.createComment(subject='subject1', vote='Approve',
                                    content='content1')
        self.assertApproved()


class TestGitlabProposals(unittest.TestCase):

    maxDiff = None  # Errors can be verbose

    def setUp(self):
        super().setUp()
        fixtures.use_gitlab(self)
        self.branch_handler = fixtures.GitlabBranchHandler()
        self.branch_handler.set_identity(self)
        self.branch_handler.set_gitlab_access(self)
        fixtures.setup_gitlab_proposal_target(self)
        self.proposal_handler = fixtures.GitlabProposalHandler()

    def test_no_proposals(self):
        project_name = self.branch_handler.get_project_name()
        proposals = self.gl_dev.get_proposals(project_name,
                                              self.target_branch_name)
        self.assertEqual([], proposals)

    def test_create_simple_proposal(self):
        proposal = fixtures.create_gitlab_proposal(self, 'proposal-1')
        self.assertEqual('opened', proposal['state'])


class TestGitlabProposalTesting(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.use_gitlab(self)
        self.branch_handler = fixtures.GitlabBranchHandler()
        self.branch_handler.set_identity(self)
        self.branch_handler.set_gitlab_access(self)
        fixtures.setup_gitlab_proposal_target(self)
        self.proposal_handler = fixtures.GitlabProposalHandler()
        self.proposal = fixtures.create_gitlab_proposal(self, 'testing')

    def test_not_tested(self):
        self.assertTrue('tests-pass' not in self.proposal['labels'])
        self.assertTrue('tests-fail' not in self.proposal['labels'])
        self.assertTrue('testing' not in self.proposal['labels'])

    def test_proposal_under_test(self):
        project_name = self.branch_handler.get_project_name()
        self.gl_dev.mark_proposal(project_name, self.proposal['iid'],
                                  'testing')
        updated = self.gl_dev.get_proposal(project_name, self.proposal['iid'])
        self.assertTrue('testing' in updated['labels'])

    def test_proposal_pass_tests(self):
        project_name = self.branch_handler.get_project_name()
        self.gl_dev.mark_proposal(project_name, self.proposal['iid'],
                                  'tests-pass')
        updated = self.gl_dev.get_proposal(project_name, self.proposal['iid'])
        self.assertTrue('tests-pass' in updated['labels'])

    def test_proposal_fail_tests(self):
        project_name = self.branch_handler.get_project_name()
        self.gl_dev.mark_proposal(project_name, self.proposal['iid'],
                                  'tests-fail')
        updated = self.gl_dev.get_proposal(project_name, self.proposal['iid'])
        self.assertTrue('tests-fail' in updated['labels'])


class TestGitlabProposalVotes(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.use_gitlab(self)
        self.branch_handler = fixtures.GitlabBranchHandler()
        self.branch_handler.set_identity(self)
        self.branch_handler.set_gitlab_access(self)
        fixtures.setup_gitlab_proposal_target(self)
        self.proposal_handler = fixtures.GitlabProposalHandler()
        self.proposal = fixtures.create_gitlab_proposal(self, 'testing')

    def test_no_votes(self):
        self.assertEqual('can_be_merged', self.proposal['merge_status'])
        self.assertEqual(0, self.proposal['upvotes'])
        self.assertEqual(0, self.proposal['downvotes'])

    def test_approved(self):
        project_name = self.branch_handler.get_project_name()
        self.gl_reviewer.create_proposal_comment(
            project_name, self.proposal['iid'], 'Good stuff\n/award :+1:')
        updated = self.gl_dev.get_proposal(project_name, self.proposal['iid'])
        self.assertEqual(1, updated['upvotes'])

    def test_disapproved(self):
        project_name = self.branch_handler.get_project_name()
        self.gl_reviewer.create_proposal_comment(
            project_name, self.proposal['iid'], 'Needs fixing\n/award :-1:')
        updated = self.gl_dev.get_proposal(project_name, self.proposal['iid'])
        self.assertEqual(1, updated['downvotes'])
