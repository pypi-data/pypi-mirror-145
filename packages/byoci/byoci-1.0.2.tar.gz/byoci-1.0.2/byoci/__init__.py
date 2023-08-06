# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
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

import contextlib
import os

# A tuple containing the five components of the version number: major, minor,
# micro, releaselevel, and serial. All values except releaselevel are integers;
# the release level is 'dev' or 'final'. The version_info value corresponding
# to the byoci version 2.0 is (2, 0, 0, 'final', 0).
__version__ = (1, 0, 2, 'final', 0)


def version(ver=None):
    if ver is None:
        ver = __version__
    major, minor, patch, ver_type, increment = ver
    if ver_type == 'final':
        return '{}.{}.{}'.format(major, minor, patch)
    else:
        return '{}.{}.{}{}{}'.format(*ver)


@contextlib.contextmanager
def working_directory(new):
    """A context manager preserving working directory."""
    previous = os.getcwd()
    os.chdir(new)
    try:
        yield
    finally:
        os.chdir(previous)
