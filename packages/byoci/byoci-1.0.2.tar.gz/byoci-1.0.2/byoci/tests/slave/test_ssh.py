# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
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


import errno
import os
import signal
import unittest


from byoci.slave import ssh
from byoci.tests.slave import features


@features.requires(features.ssh_agent_feature)
class TestAgent(unittest.TestCase):

    def test_not_running(self):
        self.assertEqual(dict(SSH_AUTH_SOCK=None, SSH_AGENT_PID=None),
                         ssh.SshAgent().get_env())

    def test_start(self):
        agent = ssh.SshAgent()
        self.addCleanup(agent.stop)
        agent.start()
        self.assertIsNot(None, agent.pid)
        self.assertIsNot(None, agent.auth_sock)
        # This raises OSError(3, 'No such process') if there is no such
        # process, indicating an issue in starting the agent.
        os.kill(int(agent.pid), signal.SIGCONT)

    def test_stop(self):
        agent = ssh.SshAgent()
        self.addCleanup(agent.stop)
        agent.start()
        pid = int(agent.pid)
        os.kill(pid, signal.SIGCONT)  # The pid exists
        agent.stop()
        with self.assertRaises(OSError) as cm:
            os.waitpid(pid, os.WNOHANG)
        self.assertEqual(errno.ECHILD, cm.exception.args[0])
