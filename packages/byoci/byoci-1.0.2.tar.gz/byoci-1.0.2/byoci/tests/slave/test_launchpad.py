# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
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

import unittest


from byoci.tests.slave import fixtures


class TestLaunchpad(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.lp = fixtures.use_launchpad(self)

    def test_unknown_project(self):
        with self.assertRaises(KeyError) as cm:
            self.lp.get_project('I-dont-exist')
        self.assertEqual('I-dont-exist', cm.exception.args[0])

    def test_known_project(self):
        project = self.lp.get_project(fixtures.launchpad_test_project_name)
        self.assertEqual(fixtures.launchpad_test_project_name,
                         project.display_name)
        # FIXME: This means we need a different project to test for git being
        # the project vcs -- vila 2018-01-17
        self.assertEqual('Bazaar', project.vcs)

    def test_unknown_bzr_branch(self):
        branch = self.lp.get_bzr_branch('lp:I-dont-exist')
        self.assertIs(None, branch)

    def test_known_bzr_branch(self):
        branch = self.lp.get_bzr_branch(
            'lp:~brz/{}/trunk'.format(fixtures.launchpad_test_project_name))
        self.assertIsNot(None, branch)

    def test_unknown_git_repo(self):
        git_repo = self.lp.get_git_repo('lp:I-dont-exist')
        self.assertIs(None, git_repo)

    def test_bogus_git_repo(self):
        with self.assertRaises(ValueError):
            self.lp.get_git_repo('bogus')

    def test_known_git_repo(self):
        # This relies on manually seeded data (see doc/tests.rst) and can fail
        # if qastaging is reset
        git_repo = self.lp.get_git_repo(
            'lp:{}'.format(fixtures.launchpad_test_project_name))
        self.assertIsNot(None, git_repo)
        self.assertEqual('~brz/{}/'
                         '+git/master'.format(
                             fixtures.launchpad_test_project_name),
                         git_repo.unique_name)
