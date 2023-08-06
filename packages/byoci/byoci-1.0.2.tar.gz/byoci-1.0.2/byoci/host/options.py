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

from byoci import options
from byov import subprocesses

HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


# Official API
register = options.register
option_registry = options.option_registry


######################################################################
# byoci options
######################################################################
register(options.Option('byoci', default=options.MANDATORY,
                        help_string='''\
The byoci namespace is used to defined the whole byoci setup for code as
well as the users (or launchpad teams where appropriate) responsible for the
various parts: administration, code landings and running jobs.

This allow several sets of configuration to be defined addressing different
needs (production, testing, selftest).'''))


# The branches defining a byoci setup
# FIXME: For now, it's a hard constraint to use /byoci to work around lxd
# mounting sub directories under home breaking access rights for cloud-init
# /creating/ the home dir. All sort of fun ensues... -- vila 2018-02-06
register(options.Option('byoci.definition', default='/byoci',
                        help_string='''\
The path in vms where byoci branch is installed.
'''))
register(options.Option('byoci.host.definition', default=BRANCH_ROOT,
                        help_string='''\
The path on host where byoci branch is installed.
'''))
register(options.Option('byoci.definition.branch', default=options.MANDATORY,
                        help_string='''\
The url for the byoci {byoci.prefix} branch.
'''))
register(options.Option('byoci.secrets', default='/byoci-secrets',
                        help_string='''\
The path in slave vms where secrets are stored.
'''))
register(options.Option('byoci.host.secrets', default=options.MANDATORY,
                        help_string='''\
The path on host where secrets are stored.
'''))
register(options.Option('byoci.secrets.branch', default=options.MANDATORY,
                        help_string='''\
The url for the secrets {byoci.prefix} branch.
'''))

# The machines
register(options.Option('byoci.master', default=options.MANDATORY,
                        help_string='''\
The name of the master jenkins host.
'''))
# The host managing plugins and jobs
register(options.Option('byoci.monitor', default=options.MANDATORY,
                        help_string='''\
The name of the monitor host.
'''))
register(options.ListOption('byoci.slaves', default=options.MANDATORY,
                            help_string='''\
Jenkins slave names.
'''))
# The urls to reach the master.
register(options.Option('byoci.master.url', default=options.MANDATORY,
                        help_string='''\
The http[s] url where the jenkins master is.
'''))
register(options.Option('byoci.master.api', default='{{byoci}.master.url}',
                        help_string='''\
The http[s] url where the jenkins master replies to API calls.
'''))
# The ssh keys
register(options.Option('byoci.master.ssh.key',
                        default='jenkins@{byoci.prefix}-master-{byoci}',
                        help_string='''\
The name of the master ssh key to connect to slaves.
'''))
# FIXME: Same key for all slaves ? -- vila 2018-02-14
register(options.Option('byoci.slave.ssh.key',
                        default='jenkins@{byoci.prefix}-slave-{byoci}',
                        help_string='''\
The name of the slave ssh key to connect to launchpad.
'''))


# The people
register(options.Option('byoci.admin.users', default=options.MANDATORY,
                        help_string='''\
The launchpad logins for admins on the jenkins master (web and API access).
'''))
register(options.Option('byoci.admin.email', default='jenkins@localhost',
                        help_string='''\
The email used by jenkins to report issues.
'''))
register(options.Option('byoci.monitor.user', default=options.MANDATORY,
                        help_string='''\
The jenkins API login used to maintain job and slave definitions.
'''))
register(options.Option('byoci.monitor.token', default=options.MANDATORY,
                        help_string='''\
The jenkins API token used to maintain job definitions.
'''))

# Credentials for the gatekeeper (the bot landing the proposals). This requires
# write access to the project branches on launchpad.
register(options.Option('byoci.landing.user', default=options.MANDATORY,
                        help_string='''\
The gatekeeper (landing the proposals) launchpad login.
'''))
register(options.Option('byoci.landing.fullname', default=options.MANDATORY,
                        help_string='''\
The gatekeeper (landing the proposals) full name.
'''))
register(options.Option('byoci.landing.email', default=options.MANDATORY,
                        help_string='''\
The gatekeeper (landing the proposals) email.
'''))

######################################################################
# launchpad options (in addition to the ones defined in ../options.py)
######################################################################


register(options.Option('launchpad.sso.url',
                        default='https://login.ubuntu.com',
                        help_string='''\
The launchpad single sign on url.'''))


def register_namespace(namespace, defaults):
    """Create all byoci options for a given namespace and defaults."""
    for oname in [o for o in options.option_registry.keys()
                  if o.startswith('byoci.')]:
        jopt = options.option_registry.get(oname)
        _, name = oname.split('.', 1)
        default = defaults.get(name, jopt.default)
        register(jopt.__class__(namespace + '.' + name, default=default,
                                help_string=jopt._help))


def default_brz_email():
    # FIXME: 'cd' is needed when running in the slave where the bzr repo is not
    # mounted -- vila 2018-10-21
    whoami_cmd = ['sh', '-c', 'cd && bzr whoami --email']
    ret, out, err = subprocesses.run(whoami_cmd)
    return out.strip()


def default_brz_fullname():
    # FIXME: 'cd' is needed when running in the slave where the bzr repo is not
    # mounted -- vila 2018-10-21
    whoami_cmd = ['sh', '-c', 'cd && bzr whoami']
    ret, out, err = subprocesses.run(whoami_cmd)
    fullname, _ = out.split(' <', 1)
    return fullname


register_namespace('production', {})

_testing_defaults = {
    # The user running the tests should have a valid 'bzr whoami'.  There are
    # edge cases where a host may fail to provide a valid default email but
    # then several tests will yell and the fix is easy enough: run 'bzr whoami
    # "Me <me@example.com>"'
    'landing.fullname': default_brz_fullname(),
    'landing.email': default_brz_email(),
    # The branches should be defined but empty so that scripts know that they
    # deal with mounted file systems.
    'definition.branch': '',
    'secrets.branch': '',
}
register_namespace('testing', _testing_defaults)


_selftest_defaults = _testing_defaults.copy()
_selftest_defaults.update({
    'host.secrets': '{testing.host.secrets}',
    # Just share the testing ssh keys
    'master.ssh.key': 'jenkins@{byoci.prefix}-master-testing',
    'slave.ssh.key': 'jenkins@{byoci.prefix}-slave-testing',
})
register_namespace('selftest', _selftest_defaults)
