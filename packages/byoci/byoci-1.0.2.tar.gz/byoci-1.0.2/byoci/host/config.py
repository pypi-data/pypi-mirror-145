# This file is part of  Build Your Own CI
#

# Copyright 2017, 2018 Vincent Ladeuil
# Copyright 2016, 2017 Canonical Ltd.
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

from byov import config

HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

# Official API
VmStack = config.VmStack
config_file_basename = config.config_file_basename
