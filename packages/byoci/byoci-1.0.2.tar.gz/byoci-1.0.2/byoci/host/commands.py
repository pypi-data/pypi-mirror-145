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


import logging
import os
import re
import sys


import byov
from byoc import errors
from byoci import commands
from byov import (
    config,
    commands as vms_commands,
    options,
    subprocesses,
)


logger = logging.getLogger(__name__)
setup_logging = commands.setup_logging


# FIXME: The trick is dirty: by importing byov.commands, vm_class_registry is
# populated and byov.config.import_user_byovs() is called, also populating byov
# options. A better way is needed -- vila 2018-10-19
vms_commands = vms_commands  # Please pep8


class ArgParser(commands.ArgParser):
    """An argument parser for the byo-ci-monitor script."""

    script_name = 'byo-ci-host'


# All commands are registered here, defining what run() supports
command_registry = commands.CommandRegistry()


class Help(commands.Help):

    name = 'help'
    description = 'Describe byo-ci-host commands.'
    command_registry = command_registry
    arg_parser_class = ArgParser


command_registry.register(Help)


class SetupSecrets(object):
    """The secrets needed to setup byoci."""
    def __init__(self, byoci):
        self.conf = config.VmStack(None)
        # Light hack to work around 'byoci' being provided to commands and
        # the need to get a valid config stack
        # FIXME: This forces usage from ci.breezy-vcs.org to renew ssh keys
        # and is linked to byoc.stores.Cmdline_Store not being shared which is
        # arguable -- vila 2018-10-26
        self.conf.cmdline_store.from_cmdline(['byoci={}'.format(byoci)])

    def master_key(self):
        basename = self.conf.expand_options('{{byoci}.master.ssh.key}')
        path = os.path.join(
            self.conf.expand_options('{{byoci}.host.secrets}'),
            'master', 'ssh', 'keys', basename)
        return (basename, path)

    def slave_key(self):
        basename = self.conf.expand_options('{{byoci}.slave.ssh.key}')
        path = os.path.join(
            self.conf.expand_options('{{byoci}.host.secrets}'),
            'slaves', 'ssh', 'keys', basename)
        return (basename, path)


class Secrets(commands.Command):

    name = 'secrets'
    description = 'Create missing secrets.'
    command_registry = command_registry
    arg_parser_class = ArgParser

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            '--option', '-O', metavar='OPTION=VALUE',
            action='append', dest='overrides', default=[],
            help='Override OPTION with provided VALUE. Can be repeated.')
        self.parser.add_argument(
            '--check',
            action='store_true',
            help='Check that secrets are available without creating them.')
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

    def check_key(self, name, path):
        return os.path.exists(path) and os.path.exists(path + '.pub')

    def check_or_create(self, name, path):
        exists = self.check_key(name, path)
        if self.options.check:
            if not exists:
                logger.error('Missing {}'.format(path))
                return 1
            return 0
        if exists:
                return 0
        logger.info('Generating {}'.format(name))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        gen_cmd = ['ssh-keygen', '-f', path, '-N', '',
                   '-t', 'rsa', '-b', '4096', '-C', name]
        subprocesses.run(gen_cmd)
        return 0

    def run(self):
        # FIXME: OAuth lp token ? -- vila 2018-03-02
        secrets = SetupSecrets(self.conf.get('byoci'))
        ret = self.check_or_create(*secrets.master_key())
        ret += self.check_or_create(*secrets.slave_key())
        return ret


command_registry.register(Secrets)


# FIXME: Worth back-porting to byoc requiring a stack as a parameter, could be
# a stack method ?  -- vila 2018-02-18
def matching_options(name, option_regexps):
    """Return a dict of options for a given vm and context.

    :param name: The vm name.

    :param option_regexps: The regular expressions defining the desired
        options.

    :returns: A dict of all options (and their values) matching one of the
        provided regular expressions.

    """
    conf = config.VmStack(name)
    names = [re.compile(regexp) for regexp in option_regexps]
    matching = dict()
    # Iterate over all registered options
    for opt in options.option_registry.values():
        value = None
        for regexp in names:
            if regexp.search(opt.name) is not None:
                try:
                    value = conf.get(opt.name, expand=True, convert=False)
                except errors.OptionMandatoryValueError:
                    pass
                # First match wins
                break
        if value is not None:
            # There is a defined value for that option
            matching[opt.name] = value
    # Iterate on all options defined in any store. This will catch options that
    # are not registered but defined in one store.
    for (store, section, name, a_value) in conf.iter_options():
        if matching.get(name, None) is not None:
            # We already know the value for that option
            continue
        value = None
        for regexp in names:
            if regexp.search(name) is not None:
                # First match wins
                value = conf.get(name, expand=True, convert=False)
                if value is None:
                    try:
                        opt = options.option_registry.get(name)
                    except KeyError:
                        break
                    try:
                        # Get the default value
                        value = opt.get_default()
                    except errors.OptionMandatoryValueError:
                        pass
                break
        if value is not None:
            # Takes the first defined value
            matching[name] = value
    return matching


def push_ssh_file(vm_name, name, path):
    """Push an ssh key to the given vm.

    :param name: The ssh key basename.

    :param path: The host path to the key.
    """
    dst = os.path.join('~', '.ssh', name)
    run_from_hook(['push', vm_name, '@' + path, dst])
    run_from_hook(['shell', vm_name, 'chmod', '600', dst])
    return dst


# FIXME: This doesn't fit really well here but most hooks would need to
# re-implement this to get shell '-e' behavior: fail at first error.
# -- vila 2018-02-18
def run_from_hook(args):
    logger.debug('running: {} with byov.path: {}'.format(args, byov.path))
    ret, out, err = subprocesses.run(['byov'] + args)
    logger.debug('stdout: {}'.format(out))
    logger.debug('sterr: {}'.format(err))
    if ret:
        logger.debug('{} failed with: {}'.format(args, ret))
        sys.exit(ret)
    logger.debug('{} returned: {}'.format(args, ret))
    return ret, out, err


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
