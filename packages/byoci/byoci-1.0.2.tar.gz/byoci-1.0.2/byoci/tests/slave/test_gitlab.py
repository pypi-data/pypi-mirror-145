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
import unittest


from byoci.slave import gitlab
from byoci.tests.slave import fixtures


class TestGitlabProjects(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.use_gitlab(self)

    def get_test_project_name(self):
        return os.path.join(fixtures.gitlab_test_project_path,
                            fixtures.gitlab_test_project_name)

    def test_unknown_project(self):
        with self.assertRaises(gitlab.GitlabAPIException) as cm:
            self.gl_dev.get_project('I-dont-exist')
        self.assertEqual('I-dont-exist', cm.exception.args[0])

    def test_known_project(self):
        project_name = self.get_test_project_name()
        project = self.gl_dev.get_project(project_name)
        self.assertEqual(project_name, project['path_with_namespace'])

    def test_unknown_branch(self):
        project_name = self.get_test_project_name()
        with self.assertRaises(gitlab.GitlabAPIException) as cm:
            self.gl_dev.get_branch(project_name, 'I-dont-exist')
        self.assertEqual((project_name, 'I-dont-exist'), cm.exception.args[0])

    def test_known_branch(self):
        branch = self.gl_dev.get_branch(self.get_test_project_name(), 'master')
        self.assertIsNot(None, branch)
