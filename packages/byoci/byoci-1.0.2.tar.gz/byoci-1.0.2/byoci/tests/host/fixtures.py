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
import shutil


import byov
from byoci.host import config
from byoci.tests import fixtures
from byoci.tests.host import (
    assertions,
    features,
)
from byov import (
    commands as vms_commands,
    config as vms_config,
)


HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))

# Useful shortcuts
patch = fixtures.patch

# Make sure user (or system) defined environment variables do not leak in the
# test environment.
isolated_environ = {
    'HOME': None,
}


def isolate_from_disk_for_host(test):
    """Provide an isolated disk-based environment.

    A $HOME directory is setup so tests can setup arbitrary files including
    config ones.
    """
    # Preserve some options from the outer environment
    outer = config.VmStack(None)
    # FIXME: One place to fix to better handle sso/ldap launchpad/gitlab
    # -- vila 2018-08-08
    lp_login = outer.get('launchpad.login')
    gl_login = outer.get('gitlab.login')
    # If there is a gitlab test server
    # FIXME: hard-coded vm name -- vila 2018-09-19
    gitlab_conf = config.VmStack('gitlab')
    if features.gitlab_test_server.available():
        gitlab_api_url = gitlab_conf.get('gitlab.api.url')
    else:
        gitlab_api_url = ''
    # FIXME: These options are badly named (not precise enough) and not stored
    # in the right place -- vila 2018-08-07
    ldap_user = outer.get('ldap.user')
    ldap_password = outer.get('ldap.password')

    ssh_key = outer.get('ssh.key')
    byoci_prefix = outer.get('byoci.prefix')

    # Switch the current dir to something unique
    fixtures.set_uniq_cwd(test)
    # Share the lxd certificate. We could generate one on the fly but assume
    # instead that one is already available since we require the lxc client
    # already.
    lxd_conf_dir = os.path.expanduser('~/.config/lxc')
    # Isolate tests from the user environment
    fixtures.isolate_from_env(test, isolated_environ)
    test.home_dir = os.path.join(test.uniq_dir, 'home')
    os.mkdir(test.home_dir)
    fixtures.override_env(test, 'HOME', test.home_dir)
    fixtures.override_env(test, 'BZR_HOME', test.home_dir)
    fixtures.override_env(test, 'LXD_CONF', lxd_conf_dir)
    patch(test, byov, 'path', byov.path + [test.uniq_dir])
    fixtures.override_env(test, 'BYOV_PATH', ':'.join(byov.path))
    fixtures.set_bzr_identity(test)
    inner = config.VmStack(None)
    inner.set('byoci', 'selftest')
    # Inject preserved options
    inner.set('launchpad.login', lp_login)
    inner.set('gitlab.login', gl_login)
    inner.set('gitlab.api.url', gitlab_api_url)
    # FIXME: Make sure those are truly optional -- vila 2018-11-23
    if ldap_user:
        inner.set('ldap.user', ldap_user)
    if ldap_password:
        inner.set('ldap.password', ldap_password)
    inner.set('ssh.key', ssh_key)
    inner.set('byoci.prefix', byoci_prefix)
    # Also isolate from the system environment
    test.etc_dir = os.path.join(test.uniq_dir,
                                vms_config.system_config_dir()[1:])
    os.makedirs(test.etc_dir)
    fixtures.patch(test, vms_config, 'system_config_dir',
                   lambda: test.etc_dir)

    # Pre-define some vm names to be unique
    def unique_name(seed):
        fmt = '{byoci.prefix}-{seed}-{byoci}-{pid}'
        return inner.expand_options(fmt, env=dict(seed=seed,
                                                  pid=str(os.getpid())))
    test.master_name = unique_name('master')
    inner.set('selftest.master', test.master_name)
    test.monitor_name = unique_name('monitor')
    inner.set('selftest.monitor', test.monitor_name)
    test.slave_name = unique_name('slave')
    # A single slave will do
    inner.set('selftest.slaves', test.slave_name)

    # Source access
    inner.set('selftest.host.definition', BRANCH_ROOT)
    # Saving the config creates the missing dirs (~/.config/byov) in the tmp
    # test dir
    inner.store.save()
    inner.store.unload()

    test.conf = inner
    return outer, inner


def setup_byoci_conf(test):
    """Setup byoci selftest config files.

    This allows tests to get access to all vm definitions composing a byoci
    setup.
    """
    features.test_requires(test, features.tests_config)
    etc_confd_dir = os.path.join(test.etc_dir, 'conf.d')
    os.mkdir(etc_confd_dir)
    os.mkdir('byov.conf.d')
    for rank, root in enumerate(byov.path):
        sct = os.path.join(root, 'byov.conf.d/selftest.conf-tests')
        if os.path.exists(sct):
            name = 'selftest' + str(rank) + '.conf'
            os.symlink(sct, os.path.join('byov.conf.d', name))

    # Make user provided test config files visible to tests by installing them
    # under self.home_dir/.config/byov/conf.d
    user_confd_dir = os.path.join(test.home_dir, '.config', 'byov', 'conf.d')
    os.makedirs(user_confd_dir)

    def install(src, dst):
        with open(src) as s, open(dst, 'w') as d:
            d.write(s.read())
    # Since ~/.config/byov/byov.conf is easier to use for tests themselves, it
    # makes sense to divert the outer ~/.config/byov/byov.conf to
    # /etc/byov/byov.conf
    install(features.tests_config.user_path,
            os.path.join(etc_confd_dir, config.config_file_basename()))
    if features.tests_config.more_paths:
        for p in features.tests_config.more_paths:
            _, bname = os.path.split(p)
            # Drop the -tests suffix from the basename
            install(p, os.path.join(user_confd_dir, bname[:-len('-tests')]))

    # setup byov to include the files created above
    fixtures.override_env(test, 'BYOV_PATH', ':'.join(byov.path))
    vms_config.import_user_byov_from(test.uniq_dir)

    test.setup_cmd = vms_commands.Setup(out=test.out, err=test.err)
    test.teardown_cmd = vms_commands.Teardown(out=test.out, err=test.err)


def setup_secrets(test):
    """Duplicate existing secrets so tests can delete/create them."""
    conf = config.VmStack(None)
    orig = conf.get('selftest.host.secrets')
    shutil.copytree(orig, 'secrets')
    conf.set('selftest.host.secrets', os.path.join(test.uniq_dir, 'secrets'))
    conf.store.save()
    conf.store.unload()


def setup_vm(test, vm_name):
    test.addCleanup(teardown_vm, test, vm_name)
    cmd = test.setup_cmd
    args = [vm_name]
    cmd.parse_args(args)
    ret = cmd.run()
    assertions.assertShellSuccess(test, ['setup'] + args, ret,
                                  test.out, test.err)
    return ret


def teardown_vm(test, vm_name):
    cmd = test.teardown_cmd
    args = ['--force', vm_name]
    cmd.parse_args(args)
    ret = cmd.run()
    return ret


# Useful shortcuts to export
override_logging = fixtures.override_logging
