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


import argparse
import logging
import sys


from byoc import registries

logger = logging.getLogger(__name__)


def setup_logging(level=None, fmt=None):
    if level is None:
        level = logging.ERROR
    if fmt is None:
        fmt = '%(levelname)s %(message)s'
    logging.basicConfig(level=level, format=fmt)


class ArgParser(argparse.ArgumentParser):
    """An argument parser for the byo-ci- scripts."""

    script_name = 'Must be set by daughter classes'

    def __init__(self, name, description):
        super().__init__(
            prog='{} {}'.format(self.script_name, name),
            description=description)

    def parse_args(self, args=None, out=None, err=None):
        """Parse arguments, overridding stdout/stderr if provided.

        :params args: Defaults to sys.argv[1:].

        :param out: Defaults to sys.stdout.

        :param err: Defaults to sys.stderr.
        """
        out_orig = sys.stdout
        err_orig = sys.stderr
        try:
            if out is not None:
                sys.stdout = out
            if err is not None:
                sys.stderr = err
            return super().parse_args(args)
        finally:
            sys.stdout = out_orig
            sys.stderr = err_orig


class CommandRegistry(registries.Registry):
    """A registry specialized for commands."""

    def register(self, cmd):
        super().register(
            cmd.name, cmd, help_string=cmd.description)


class Command(object):

    name = 'Must be set by daughter classes'
    description = 'Must be set by daughter classes'
    arg_parser_class = ArgParser

    def __init__(self, out=None, err=None):
        """Command constructor.

        :param out: A stream for command output.

        :param err: A stream for command errors.
        """
        if out is None:
            out = sys.stdout
        if err is None:
            err = sys.stderr
        self.out = out
        self.err = err
        self.parser = self.arg_parser_class(self.name, self.description)

    def parse_args(self, args):
        self.options = self.parser.parse_args(args, self.out, self.err)
        return self.options


class Help(Command):

    name = 'help'
    description = 'Must be set by daughter classes'
    command_registry = 'Must be set by daughter classes'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'commands', metavar='COMMAND', nargs='*',
            help='Display help for each command'
            ' (All if none is given).')

    def run(self):
        if not self.options.commands:
            self.out.write('Available commands:\n')
            for cmd_name in self.command_registry.keys():
                cmd_class = self.command_registry.get(cmd_name)
                self.out.write('\t{}: {}\n'.format(cmd_class.name,
                                                   cmd_class.description))
            return
        for cmd_name in self.options.commands:
            try:
                cmd_class = self.command_registry.get(cmd_name)
            except KeyError:
                cmd_class = None
            if cmd_class:
                cmd = cmd_class()
                cmd.parser.print_help(self.out)
            else:
                msg = '"{}" is not a known command\n'.format(cmd_name)
                self.err.write(msg)
                return 1
        return 0
