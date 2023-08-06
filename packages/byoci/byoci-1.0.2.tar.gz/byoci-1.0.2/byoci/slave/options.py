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

from byov import options as vms_options

from byoci import options

# Registering the options requires importing them, this is purely declarative.
vms_options = vms_options


HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


# Official API
register = options.register

######################################################################
# Project specific options
######################################################################

register(options.Option('project.secrets', default='',
                        help_string='''\
A list of 'source:destination' files,
'source' is a path relative to '~/secrets' in the slaves,
'destination' is a path relative to 'home/{vm.user}'
inside the container.  '''))


######################################################################
# byoci options
######################################################################

_kh_path = os.path.join(BRANCH_ROOT, 'setup', 'known_hosts')
register(options.PathOption('byoci.setup_known_hosts',
                            default=_kh_path,
                            help_string='''\
The path to the script installing ~/.ssh/known_hosts in the containers
with verified keys.

This allows project containers to reach outside hosts via ssh (think code
hosting providers).
'''))
