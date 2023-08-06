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

from byoci.monitor import config
from byoci.tests import fixtures


# Make sure user (or system) defined environment variables do not leak in the
# test environment.
isolated_environ = {
    'HOME': None,
}


def isolate_from_disk_for_monitor(test):
    """Provide an isolated disk-based environment.

    A $HOME directory is setup so tests can setup arbitrary files including
    config ones.
    """
    fixtures.fixtures.set_uniq_cwd(test)
    # Preserve some options from the outer environment
    outer = config.MonitorStack()
    preserved_options = ('byoci.api', 'byoci.user', 'byoci.token',
                         'jenkins.home', 'jenkins.plugins')
    preserved_values = [outer.get(name) for name in preserved_options]
    # Isolate tests from the user environment
    fixtures.isolate_from_env(test, isolated_environ)
    test.home_dir = os.path.join(test.uniq_dir, 'home')
    os.mkdir(test.home_dir)
    fixtures.override_env(test, 'HOME', test.home_dir)
    inner = config.MonitorStack()
    # Inject preserved options
    for name, value in zip(preserved_options, preserved_values):
        inner.set(name, value)
    return outer, inner


# Useful shortcuts to export
override_logging = fixtures.override_logging
