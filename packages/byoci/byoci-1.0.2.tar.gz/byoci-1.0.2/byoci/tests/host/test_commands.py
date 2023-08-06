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
import os
import shutil
import unittest


from byot import (
    assertions,
    scenarii,
)
from byov import commands as vms_commands


from byoci.host import (
    commands,
    config,
)
from byoci.tests.host import fixtures


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
        ns = self.parse_args(['help'])
        self.assertEqual(['help'], ns.commands)

    def test_several_commands(self):
        ns = self.parse_args(['help', 'not-a-command'])
        self.assertEqual(['help', 'not-a-command'], ns.commands)


class TestHelp(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def assertHelp(self, expected, args=None):
        if args is None:
            args = []
        commands.run(['help'] + args, self.out, self.err)
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.out.getvalue())

    def test_help_wrong_command(self):
        ret = commands.run(['help', 'not-ac-command'], self.out, self.err)
        self.assertEqual(1, ret)

    def test_help_alone(self):
        self.assertHelp('''\
Available commands:
\thelp: Describe byo-ci-host commands.
\tsecrets: Create missing secrets.
''')

    def test_help_help(self):
        self.assertHelp('''\
usage: byo-ci-host... help [-h] [COMMAND [COMMAND ...]]

Describe byo-ci-host commands.

positional arguments:
  COMMAND     Display help for each command (All if none is given).

optional arguments:
  -h, --help  show this help message and exit
''',
                        ['help'])


class TestConfig(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_defaults(self):
        config_cmd = vms_commands.Config(out=self.out, err=self.err)
        cmd_args = [self.master_name, 'byoci']
        config_cmd.parse_args(cmd_args)
        ret = config_cmd.run()
        self.assertEqual(0, ret)
        self.assertEqual('selftest', self.out.getvalue())


class TestMatchingOptions(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.override_logging(self)

    def test_empty_regexps(self):
        self.assertEqual(dict(),
                         commands.matching_options(self.slave_name, []))

    def test_simple_regexp(self):
        expected = {
            'byoci.slave.ssh.key': 'jenkins@{byoci.prefix}-slave-selftest',
            'production.slave.ssh.key':
            'jenkins@{byoci.prefix}-slave-selftest',
            'production.slaves': '{byoci.prefix}-slave-production-1',
            'selftest.slave.ssh.key': 'jenkins@{byoci.prefix}-slave-testing',
            'selftest.slaves': self.slave_name,
            'testing.slave.ssh.key': 'jenkins@{byoci.prefix}-slave-selftest',
            'testing.slaves': '{byoci.prefix}-slave-testing'
        }
        for k, v in expected.items():
            expected[k] = self.conf.expand_options(v)
        self.assertEqual(expected,
                         commands.matching_options(self.slave_name, [
                             'selftest.slaves$', 'slave']))

    def test_multiple_regexps(self):
        self.assertEqual(
            {'selftest.master.url': 'default'},
            commands.matching_options(self.slave_name, [
                'selftest.master.url']))

    def test_byoci(self):
        self.assertEqual(
            dict(byoci='selftest'),
            commands.matching_options(self.slave_name, ['^byoci$']))

    def test_vm_name(self):
        # vm.name is a snowflake ;-)
        self.assertEqual(
            dict(),
            commands.matching_options(self.slave_name, ['^vm.name$']))

    def test_unregistered(self):
        conf = config.VmStack(self.slave_name)
        conf.set('I.am.not', 'registered')
        self.assertEqual(
            {'I.am.not': 'registered'},
            commands.matching_options(self.slave_name, ['^I.am\.']))

    def test_slave_reference(self):
        # This is slightly eager (several regexps, ignoring values, requiring
        # precise list) but establish the reference for slave design.
        expected_keys = ['launchpad.' + k for k in (
            'credentials',
            'login',
            'service_root',
            'sso.url',
        )] + ['selftest.' + k for k in (
            'admin.email',
            'admin.users',
            'definition',
            'definition.branch',
            'host.definition',
            'host.jobs',
            'host.secrets',
            'host.users',
            'landing.email',
            'landing.fullname',
            'landing.user',
            'master',
            'master.api',
            'master.ssh.key',
            'master.url',
            'monitor',
            'monitor.user',
            'prefix',
            'secrets',
            'secrets.branch',
            'slave.ssh.key',
            'slaves',
        )]
        actual_keys = sorted(commands.matching_options(
            self.slave_name, ['^selftest\.', '^launchpad\.']).keys())
        self.assertEqual(expected_keys, actual_keys)


class TestSecretsOptions(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        secrets_cmd = commands.Secrets(out=self.out, err=self.err)
        return secrets_cmd.parse_args(args)

    def test_defaults(self):
        ns = self.parse_args([])
        self.assertEqual(False, ns.check)


class TestSecrets(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk_for_host(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.setup_byoci_conf(self)
        fixtures.setup_secrets(self)
        fixtures.override_logging(self)
        self.command = commands.Secrets(out=self.out, err=self.err)
        self.secrets = commands.SetupSecrets(self.command.conf.get('byoci'))

    def run_command(self, args):
        self.command.parse_args(args)
        return self.command.run()

    def test_check_succeeds(self):
        # In the default test environment, all keys are available
        ret = self.run_command(['--check'])
        self.assertEqual(
            0, ret,
            'secrets failed with: {}\n\tstdout: {}\n\tstderr: {}'.format(
                ret, self.out.getvalue(), self.err.getvalue()))

    def test_check_no_master_key(self):
        master_key_path = self.secrets.master_key()[1]
        os.remove(master_key_path)
        self.assertEqual(1, self.run_command(['--check']))

    def test_create_master_key(self):
        master_key_path = self.secrets.master_key()[1]
        shutil.rmtree(os.path.dirname(master_key_path))
        self.assertEqual(1, self.run_command(['--check']))
        # Create the key now
        self.assertEqual(0, self.run_command([]))
        self.assertTrue(os.path.exists(master_key_path))
        self.assertTrue(os.path.exists(master_key_path + '.pub'))

    def test_check_no_slave_key(self):
        slave_key_path = self.secrets.slave_key()[1]
        os.remove(slave_key_path)
        self.assertEqual(1, self.run_command(['--check']))

    def test_create_slave_key(self):
        slave_key_path = self.secrets.slave_key()[1]
        os.remove(slave_key_path)
        self.assertEqual(1, self.run_command(['--check']))
        # Create the key now
        self.assertEqual(0, self.run_command([]))
        self.assertTrue(os.path.exists(slave_key_path))
        self.assertTrue(os.path.exists(slave_key_path + '.pub'))

    def test_check_no_keys(self):
        master = self.secrets.master_key()
        os.remove(master[1])
        slave = self.secrets.slave_key()
        os.remove(slave[1])
        self.assertEqual(2, self.run_command(['--check']))
        self.assertEqual('''Missing {}\nMissing {}\n'''.format(master[1],
                                                               slave[1]),
                         self.log_stream.getvalue())
