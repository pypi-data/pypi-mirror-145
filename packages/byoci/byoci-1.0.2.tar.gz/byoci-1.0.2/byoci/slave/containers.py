# This file is part of Build Your Own CI
#
# Copyright 2017, 2018 Vincent Ladeuil
# Copyright 2017 Canonical Ltd.
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

from __future__ import unicode_literals


import logging
import os
import subprocess
import sys

# FIXME: errors is imported so containers.errors can be used from elsewhere by
# just importing byoci.containers (rather than byov.errors). A way to
# address the long standing issue of the errors namespace may be to just make
# them attributes of the relevant classes (this would also clarify who raises
# what).  -- vila 2017-01-31
from byov import (  # noqa blurgh FIXME
    errors,
    subprocesses,
)


from byoci.slave import (
    config,
    ssh,
)


logger = logging.getLogger(__name__)


# FIXME: Maybe worth backporting to byov with tests -- vila 2017-01-25
def raw_run(args, out=None, err=None):
    """Invoke a byov command, possibly capturing the output.

    The command line tool (and its API) are used to reduce the coupling.
    """
    # If capturing, tell Popen to pipe
    stdout = subprocess.PIPE if out is not None else None
    stderr = subprocess.PIPE if err is not None else None
    logger.debug('Running {}'.format(' '.join(args)))
    proc = subprocess.Popen(args, stdout=stdout, stderr=stderr)
    # If the output and/or error are not captured, communicate() will return
    # empty strings (i.e. either output and errors pass through and are
    # displayed or they are captured by 'out' and 'err').
    cmd_out, cmd_err = proc.communicate()
    # If captured, give back
    if out is not None:
        out.write(cmd_out.decode('utf8'))
    if stderr is not None:
        err.write(cmd_err.decode('utf8'))
    return proc.returncode


class Container(object):

    def __init__(self, name, out=None, err=None):
        self.name = name
        self.conf = config.VmStack(name)
        self.ssh_agent = ssh.SshAgent()
        if out is None:
            out = sys.stdout
        if err is None:
            err = sys.stderr
        self.out = out
        self.err = err

    def status(self):
        """Get container status."""
        return subprocesses.run(['byov', 'status', self.name])[1].strip()

    def setup_ssh(self):
        """Setup ssh inside the container.

        This is mostly for launchpad ssh keys.

        Note that this setup only prepare ssh, until a key is provided by an
        agent though, no ssh access to launchpad will be available.
        """
        self.shell(['@' + self.conf.get('byoci.setup_known_hosts')])

    def bzr(self, args, with_agent=False):
        return self.shell(['bzr'] + args, with_agent=with_agent)

    def git(self, args):
        return self.shell(['git'] + args)

    def setup_vcs(self):
        # We *don't* setup commit identity (with {bzr.email},
        # {git.name}, {git.email} because commit happens only on the
        # slave. If the case arise, a --with-identity option will be
        # needed.
        lp_login = self.conf.get('launchpad.login')

        try:
            self.shell(['test', '-f', '/usr/bin/bzr'])
        except errors.CommandError:
            pass
        else:
            self.bzr(['lp-login', lp_login], with_agent=True)

        ssh_lp = 'url.ssh://{}@git.launchpad.net/.insteadOf'.format(lp_login)

        def instead_of(url):
            self.git(['config', '--global', '--add', ssh_lp, url])

        try:
            self.shell(['test', '-f', '/usr/bin/git'])
        except errors.CommandError:
            pass
        else:
            instead_of('lp:')
            instead_of('git+ssh://git.launchpad.net/')
            instead_of('ssh://git.launchpad.net/')

    def setup(self, args=None):
        """Setup container from its byov configuration.

        :param args: A list of additional options for byov setup.
        """
        if args is None:
            args = []
        setup_command = ['byov', 'setup'] + args + [self.name]
        ret = self.raw_run(setup_command)
        if ret:
            # if self.out or self.err are not set to sys.std{out,err}, they may
            # contain useful information.
            if self.out == sys.stdout:
                out = 'sent to stdout'
            else:
                out = self.out.getvalue()
            if self.err == sys.stderr:
                err = 'sent to stderr'
            else:
                err = self.err.getvalue()
            raise errors.CommandError(setup_command, ret, out, err)
        self.setup_ssh()
        self.inject_secrets()
        self.setup_vcs()

    def teardown(self, force=True):
        """Teardown container.

        :param force: If True (default), stops the container before teardown.
        """
        if force and self.status() == 'RUNNING':
            self.stop()
        return self.raw_run(['byov', 'teardown', self.name])

    def start(self):
        """Start the container."""
        return self.raw_run(['byov', 'start', self.name])

    def stop(self):
        """Stop the container."""
        return self.raw_run(['byov', 'stop', self.name])

    def wrap_command_and_start_agent(self, args):
        env_cmd = []
        ssh_opts = []
        self.ssh_agent.start()
        # There is only one usable ssh key on the slave, load it in the
        # agent
        self.ssh_agent.add(self.conf.get('ssh.key'))
        ssh_opts = ['-Ossh.options={},-A'.format(
            self.conf.get('ssh.options', convert=False))]
        env_cmd = ['env'] + ['{}={}'.format(k, v)
                             for k, v in self.ssh_agent.get_env().items()
                             if v is not None]

        full_command = env_cmd + ['byov', 'shell'] + ssh_opts + [
            self.name] + args
        return full_command

    def shell(self, args, with_agent=False):
        """Run a command in the container.

        Standard output and error are captured.

        :param args: A command and its arguments.

        :param with_agent: Whether an ssh agent is needed.

        :raises errors.CommandError: If the command ends with a non-zero return
            code.
        """
        try:
            if with_agent:
                full_command = self.wrap_command_and_start_agent(args)
            else:
                full_command = ['byov', 'shell', self.name] + args
            return subprocesses.run(full_command)
        finally:
            if with_agent:
                self.ssh_agent.stop()

    def raw_shell(self, args, with_agent=False):
        """Run a command in the container.

        :param args: A command and its arguments.

        :param with_agent: Whether an ssh agent is needed.
        """
        try:
            if with_agent:
                full_command = self.wrap_command_and_start_agent(args)
            else:
                full_command = ['byov', 'shell', self.name] + args
            return self.raw_run(full_command)
        finally:
            if with_agent:
                self.ssh_agent.stop()

    def raw_run(self, args):
        out = None if self.out == sys.stdout else self.out
        err = None if self.err == sys.stderr else self.err
        return raw_run(args, out=out, err=err)

    # FIXME: We shouldn't need the command-line access to the config anymore
    # -- vila 2017-02-02
    def config(self, args):
        """Get or set container configuration."""
        return subprocesses.run(['byov', 'config', self.name] + args)[1]

    def digest(self):
        """Get the digest for the container.

        This is a hash of all setup configuration options which can be used to
        detect changes that requires the container to be rebuilt.
        """
        return subprocesses.run(['byov', 'digest', self.name])[1]

    def inject_secrets(self):
        """Inject secrets in containers that define some.

        'project.secrets' should be defined in the byoci 'byov.conf' user
        file since this is byoci specific and should not appear in the
        project itself. See 'containers/byov.conf' for details.
        """
        # FIXME: Better define as an option with the right default value ?
        # -- vila 2017-02-12
        secrets = self.conf.get('project.secrets') or ''
        for secret in secrets.split(','):
            if not secret:
                continue
            src, dst = secret.split(':')
            # FIXME: localhost {{byoci}.secrets.definition} ?
            # -- vila 2018-02-19
            src_path = os.path.join(os.path.expanduser('/byoci-secrets'), src)
            dst_path = os.path.join('/home/ubuntu', dst)
            # Ensure destination directory exist
            self.shell(['mkdir', '-p', os.path.dirname(dst_path)])
            # FIXME: Ideally byovm should define a 'push' command
            # -- vila 2017-01-23
            # FIXME: 'push' has been implemented -- vila 2018-02-19
            lxc_push_command = [
                'lxc', 'file', 'push',
                # Assumes 'ubuntu' in the container
                '--uid', '1000', '--gid', '1000',
                src_path, self.name + dst_path
            ]
            subprocesses.run(lxc_push_command)


class Worker(Container):

    def __init__(self, name, backing_name, out=None, err=None):
        super().__init__(name, out=out, err=err)
        self.backing_name = backing_name
        self.backing = None

    # Just to avoid programmer errors, there is no setup nor teardown for
    # workers
    def setup(self):
        raise NotImplementedError(self.setup)

    def teardown(self):
        raise NotImplementedError(self.teardown)

    def ensure_backing(self):
        """Ensures the backing container is up to date.

        The backing container is built if it doesn't exist or rebuilt if its
        digest has changed.
        """
        self.backing = Container(self.backing_name, out=self.out, err=self.err)
        needs_setup = False
        if self.backing.status() == 'UNKNOWN':
            needs_setup = True
        else:
            existing = self.backing.config(['vm.setup.digest'])
            current = self.backing.digest()
            if existing != current:
                needs_setup = True
        if needs_setup:
            cleanup = False
            try:
                self.backing.setup(['--force'])
            except errors.CommandError:
                # If setup() fails, don't leave the container around as it
                # can't be used anyway
                cleanup = True
                raise
            finally:
                self.backing.stop()
                if cleanup:
                    self.backing.teardown()

    def start(self, mounts=None):
        """Start the worker, updating the backing container if needed.

        :param mounts: A list of mounts (host, container) paths to setup in
            the worker.
        """
        self.ensure_backing()
        start_options = ['-Ovm.class=ephemeral-lxd',
                         '-Ovm.backing={}'.format(self.backing_name)]
        if mounts:
            start_options += ['-Olxd.user_mounts={}'.format(
                ','.join(mounts))]
        return self.raw_run(
            ['byov', 'start', self.name] + start_options)

    def stop(self):
        """Stop the worker, freeing all associated resources."""
        stop_options = ['-Ovm.class=ephemeral-lxd',
                        '-Ovm.backing={}'.format(self.backing_name)]
        return self.raw_run(
            ['byov', 'stop', self.name] + stop_options)
