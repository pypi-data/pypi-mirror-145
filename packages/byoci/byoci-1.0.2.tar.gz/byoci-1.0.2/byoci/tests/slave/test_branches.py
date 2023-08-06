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

from __future__ import unicode_literals


import os
import unittest


from byot import scenarii


from byoci.tests.slave import fixtures


load_tests = scenarii.load_tests_with_scenarios


class TestLocalBranch(unittest.TestCase):

    scenarios = [('bzr', dict(branch_handler=fixtures.BzrBranchHandler())),
                 ('git', dict(branch_handler=fixtures.GitRepositoryHandler()))]

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_slave(self)
        self.branch_handler.set_identity(self)

    def test_delete(self):
        branch = self.branch_handler.factory('branch')
        branch.create()
        self.assertTrue(os.path.exists(os.path.join(
            'branch', self.branch_handler.vcs_dir)))
        branch.delete()
        self.assertFalse(os.path.exists('branch'))

    def test_create(self):
        branch = self.branch_handler.factory('branch')
        self.addCleanup(branch.delete)
        branch.create()
        self.assertEqual('', branch.status())

    def test_update(self):
        branch = self.branch_handler.factory('branch')
        self.addCleanup(branch.delete)
        branch.create()
        branch.update('Something', 'file: foo\nfoo content\n')
        self.assertEqual('', branch.status())
        self.assertTrue(os.path.exists('branch/foo'))

    def test_last_commit_msg(self):
        branch = self.branch_handler.factory('branch')
        self.addCleanup(branch.delete)
        branch.create()
        branch.update('Something', 'file: foo\nfoo content\n')
        self.assertEqual('Something', branch.last_commit_msg())


class TestLaunchpadBranch(unittest.TestCase):

    scenarios = [('bzr', dict(branch_handler=fixtures.BzrBranchHandler())),
                 ('git', dict(branch_handler=fixtures.GitRepositoryHandler()))]

    def setUp(self):
        super().setUp()
        self.lp = fixtures.use_launchpad(self)
        self.branch_handler.set_identity(self)
        self.branch_handler.set_launchpad_access(self)

    def test_create_from(self):
        # Create a source branch on launchpad
        source = self.branch_handler.factory('source')
        self.addCleanup(source.delete)
        source.create()
        source.update('Something', 'file: foo\nfoo content\n')
        source_lp_url = self.branch_handler.lp_branch_url('source')
        source.push(source_lp_url)
        source_lp_branch = self.branch_handler.get_branch_from_lp(
            self.lp, source_lp_url)
        self.addCleanup(source_lp_branch.lp_delete)
        # Now create a local branch from the lp one
        branch = self.branch_handler.factory('branch')
        self.addCleanup(branch.delete)
        branch.create_from(source_lp_url)
        self.assertTrue(os.path.exists(os.path.join(
            'branch', self.branch_handler.vcs_dir)))

    def test_push(self):
        branch = self.branch_handler.factory('branch')
        self.addCleanup(branch.delete)
        branch.create()
        branch.update('Something', 'file: foo\ncontent\n')
        lp_url = self.branch_handler.lp_branch_url('push')
        branch.push(lp_url)
        lp_branch = self.branch_handler.get_branch_from_lp(self.lp, lp_url)
        self.addCleanup(lp_branch.lp_delete)
        self.assertEqual(lp_url[3:], lp_branch.unique_name)


class TestGitlabBranch(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.use_gitlab(self)
        self.branch_handler = fixtures.GitlabBranchHandler()
        self.branch_handler.set_identity(self)
        self.branch_handler.set_gitlab_access(self)

    def test_create_from(self):
        # Create a source branch on gitlab
        source = self.branch_handler.factory('source')
        self.addCleanup(source.delete)
        source.create()
        source.update('Something', 'file: foo\nfoo content\n')
        source_url, source_name = self.branch_handler.gl_branch_url('source')
        # FIXME: switch() shouldn't be necessary -- vila 2018-07-25
        source.switch(source_name)
        project_name = self.branch_handler.get_project_name()
        self.addCleanup(self.gl_dev.delete_branch, project_name, source_name)
        source.push(source_url, source_name)
        # Now create a local branch from the gitlab one
        branch = self.branch_handler.factory('branch')
        self.addCleanup(branch.delete)
        branch.create_from(source_url, source_name)
        self.assertTrue(os.path.exists(os.path.join(
            'branch', self.branch_handler.vcs_dir)))

    def test_push(self):
        branch = self.branch_handler.factory('branch')
        self.addCleanup(branch.delete)
        branch.create()
        branch.update('Something', 'file: foo\ncontent\n')
        url, branch_name = self.branch_handler.gl_branch_url('push')
        # FIXME: switch() shouldn't be necessary -- vila 2018-07-25
        branch.switch(branch_name)
        project_name = self.branch_handler.get_project_name()
        self.addCleanup(self.gl_dev.delete_branch, project_name, branch_name)
        branch.push(url, branch_name)
        gl_branch = self.branch_handler.get_branch_from_gl(
            self.gl_dev, project_name, branch_name)
        self.assertEqual(branch_name, gl_branch['name'])
