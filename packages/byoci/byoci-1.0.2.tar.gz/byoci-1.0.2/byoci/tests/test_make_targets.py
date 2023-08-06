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

import subprocess
import unittest

from byot import scenarii
from byoci.tests import features


load_tests = scenarii.load_tests_with_scenarios


class MakeTargetTestCase(unittest.TestCase):
    """Some tests are easier to write as make targets.

    This really is a shortcut and shouldn't replace more precise tests.

    Nevertheless, it's better to have such tests run as part of the regular
    test suite than having them run before or after the whole suite. Being able
    to run them as part of the test suite means they can be run concurrently
    rather than making the whole run slower.

    """

    scenarios = [(k, dict(target=k)) for k in ('lint',)]

    def test_target(self):
        features.test_requires(self, features.make_feature)
        # FIXME: This should apply to the 'lint' target only -- vila 2018-02-20
        features.test_requires(self, features.flake8_feature)
        make = ['make', self.target]
        try:
            subprocess.check_output(make, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf8')
            # If at least one error is found, the exception is raised. We
            # prepend a '\n' so 'AssertionError is on a line by itself.
            self.assertEqual('', output, '\n' + output)
