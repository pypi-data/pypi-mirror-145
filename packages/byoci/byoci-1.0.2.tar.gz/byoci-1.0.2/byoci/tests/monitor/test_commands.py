# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil.
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
import unittest


from byot import assertions
from byoci.monitor import (
    commands,
)
from byoci.tests.monitor import (
    features,
    fixtures,
)


# FIXME: Duplicated from ../test_commands.py but can this be fixed ?
# -- vila 2018-02-10
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
        ns = self.parse_args(['update-plugins'])
        self.assertEqual(['update-plugins'], ns.commands)

    def test_several_commands(self):
        ns = self.parse_args(['help', 'update-plugins', 'not-a-command'])
        self.assertEqual(['help', 'update-plugins', 'not-a-command'],
                         ns.commands)


# FIXME: ~Duplicated from ../test_commands.py but can this be fixed ?
# -- vila 2018-02-10
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
\thelp: Describe byo-ci-monitor commands.
\trun-job: Run job[s].
\tupdate-plugins: Update master plugins.
\tupdate-slave: Update slave.
''')

    def test_help_help(self):
        self.assertHelp('''\
usage: byo-ci-monitor... help [-h] [COMMAND [COMMAND ...]]

Describe byo-ci-monitor commands.

positional arguments:
  COMMAND     Display help for each command (All if none is given).

optional arguments:
  -h, --help  show this help message and exit
''',
                        ['help'])


class TestUpdatePluginsOptions(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        help_cmd = commands.UpdatePlugins(out=self.out, err=self.err)
        return help_cmd.parse_args(args)

    def test_defaults(self):
        options = self.parse_args([])
        self.assertEqual([], options.overrides)


class TestUpdatePlugins(unittest.TestCase):

    def setUp(self):
        super().setUp()
        features.test_requires(self, features.master_credentials)
        fixtures.isolate_from_disk_for_monitor(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        self.command = commands.UpdatePlugins(out=self.out, err=self.err)

    def run_command(self, args):
        self.command.parse_args(args)
        return self.command.run()

    def test_succeeds(self):
        # Smoke test
        # FIXME: There is no plugins in the default config -- vila 2018-02-11
        ret = self.run_command([])
        self.assertEqual(0, ret)


class TestRunJobOptions(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        help_cmd = commands.RunJob(out=self.out, err=self.err)
        return help_cmd.parse_args(args)

    def test_defaults(self):
        options = self.parse_args(['job-regexp'])
        self.assertEqual('job-regexp', options.jobre)
        self.assertEqual(False, options.dry_run)

    def test_dry_run(self):
        options = self.parse_args(['-n', 'job-regexp'])
        self.assertEqual('job-regexp', options.jobre)
        self.assertEqual(True, options.dry_run)
