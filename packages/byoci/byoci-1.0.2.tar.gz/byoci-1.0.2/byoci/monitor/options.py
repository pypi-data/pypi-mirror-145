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
import sys


from byoci import options

register = options.register

register(options.Option('byoci.url', default=options.MANDATORY,
                        help_string='''The byoci url to use.'''))
register(options.Option('byoci.user', default=options.MANDATORY,
                        help_string='''The user API login.'''))
register(options.Option('byoci.token', default=options.MANDATORY,
                        help_string='''The user API token.'''))

register(options.Option('jenkins.home', default=options.MANDATORY,
                        help_string='''\
The jenkins home directory on the master.'''))

register(options.Option('slave', default=options.MANDATORY,
                        help_string='''\
The slave name.

This is generally set by commands so it can be used in various expansions.
'''))
# FIXME: <slave>~{vm.user} would be better -- vila 2018-02-16
register(options.Option('slave.remote.fs', default='/home/ubuntu',
                        help_string='''\
The directory used at the slave to start jobs.'''))
register(options.Option('slave.start',
                        default='\
{jenkins.home}/bin/start-slave-via-ssh {slave}',
                        help_string='''\
The command to use on the master to start a slave.
'''))
register(options.Option('slave.demand.delay', default='0',
                        help_string='''\
The delay (in minutes) before starting a slave.'''))
register(options.Option('slave.idle.delay', default='5',
                        help_string='''\
The delay (in minutes) before stopping a slave.'''))


######################################################################
# logging options (shamelessly copied from byov)
######################################################################
def level_from_store(s):
    val = None
    try:
        # Yes, _levelNames and _nameToLevel are private, but better use a
        # private than duplicate its content and get out of date.
        if sys.version_info < (3,):
            valid_levels = logging._levelNames
        else:
            valid_levels = logging._nameToLevel
        val = valid_levels[s.upper()]
    except KeyError:
        pass
    return val


register(options.Option('logging.level', default='INFO',
                        from_unicode=level_from_store,
                        help_string='''\
Logging level (same as python: error, warning, info, debug).'''))

register(options.Option('logging.format',
                        default='%(asctime)s %(levelname)s %(message)s',
                        help_string='''\
Logging format (see python doc).'''))
