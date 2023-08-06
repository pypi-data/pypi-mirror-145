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


from byov import subprocesses


class SshAgent(object):

    def __init__(self):
        self._reset()

    def _reset(self):
        self.pid = None
        self.auth_sock = None

    def start(self):
        # C-shell output is easier to scan
        _, out, _ = subprocesses.run(['ssh-agent', '-c'])
        for line in out.splitlines():
            if line.startswith('echo '):
                continue
            if line.startswith('setenv '):
                _, name, value = line.split()
                value = value.rstrip(';')
                if name == 'SSH_AUTH_SOCK':
                    self.auth_sock = value
                elif name == 'SSH_AGENT_PID':
                    self.pid = value

    def add(self, key_path):
        subprocesses.run(['env', 'SSH_AUTH_SOCK={}'.format(self.auth_sock),
                          'ssh-add', key_path])

    def stop(self):
        if self.pid is None:
            return
        subprocesses.run(['env', 'SSH_AGENT_PID={}'.format(self.pid),
                          'ssh-agent', '-k'])
        self._reset()

    def get_env(self):
        """Get the environment variables allowing agent use.

        :return: A dict with SSH_AUTH_SOCK and SSH_AGENT_PID.
        """
        return dict(SSH_AUTH_SOCK=self.auth_sock, SSH_AGENT_PID=self.pid)
