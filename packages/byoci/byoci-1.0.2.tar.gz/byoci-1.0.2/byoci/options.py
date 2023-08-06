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

from byoc import options

# Official API
Option = options.Option
ListOption = options.ListOption
PathOption = options.PathOption
MANDATORY = options.MANDATORY
option_registry = options.option_registry
register = options.register

HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..'))

register(Option('byoci.prefix', default='brz',
                help_string='''\
The prefix used by byoci vm names.'''))

# Some options are shared between host and slaves

######################################################################
# launchpad options
######################################################################

register(Option('launchpad.service_root', default='production',
                help_string='''\
The launchpad service root to talk to.'''))

register(PathOption('launchpad.credentials',
                    default='~/.config/launchpad/production',
                    help_string='''\
The path for the launchpad OAuth token.'''))


######################################################################
# gitlab options
######################################################################

register(Option('gitlab.api.url',
                help_string='''\
The gitlab url to talk to.'''))

register(PathOption('gitlab.api.credentials',
                    default='~/.config/gitlab/credentials',
                    help_string='''\
The path for the gitlab token.'''))

register(ListOption('gitlab.api.timeouts',
                    default='2, 600, 10',
                    help_string='''\
A timeouts tuple to use when talking to the gitlab API.

(first, up_to, retries):
- first: seconds to wait after the first attempt
- up_to: seconds after which to give up
- retries: how many attempts after the first try
'''))
