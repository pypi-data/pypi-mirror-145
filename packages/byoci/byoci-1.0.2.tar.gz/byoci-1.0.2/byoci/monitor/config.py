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

from byoc import (
    stacks,
    stores,
)

# Registering the options requires importing them, this is purely declarative.
from byoci.monitor import options
options = options

MonitorStore = stores.FileStore
MonitorCmdLineStore = stores.CommandLineStore


def user_config_dir():
    return os.path.expanduser('~/.config/byoci')


def config_file_basename():
    return 'byoci.conf'


class MonitorStack(stacks.Stack):

    def __init__(self):
        self.cmdline_store = MonitorCmdLineStore()
        user_path = os.path.join(user_config_dir(),
                                 config_file_basename())
        store = self.get_shared_store(MonitorStore(user_path))
        section_getters = [self.cmdline_store.get_sections,
                           stacks.NameMatcher(store, None).get_sections]
        super().__init__(section_getters, store, mutable_section_id=None)
