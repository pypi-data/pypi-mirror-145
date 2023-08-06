#!/usr/bin/env python3

# This file is part of Build Your Own Virtual machine.
#
# Copyright 2022 Vincent Ladeuil.
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
import setuptools


import byoci


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./byoci.egg-info')


setuptools.setup(
    name='byoci',
    version='.'.join(str(c) for c in byoci.__version__[0:3]),
    description=('Build Your Own Continuous Integration.'),
    author='Vincent Ladeuil',
    author_email='vincent.ladeuil@shiphero.com',
    url='https://launchpad.net/byoci',
    license='GPLv3',
    install_requires=['byov'],
    packages=['byoci', 'byoci.host', 'byoci.monitor', 'byoci.slave',
              'byoci.tests', 'byoci.tests.host', 'byoci.tests.monitor',
              'byoci.tests.slave'],
    entry_points=dict(
        console_scripts=['byo-ci-host=byoci.host.commands:run',
                         'byo-ci-monitor=byoci.monitor.commands:run',
                         'byo-ci-slave=byoci.slave.commands:run']),
    cmdclass=dict(clean=CleanCommand),
)
