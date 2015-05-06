#   Copyright (c) 2013-2015, Intel Performance Learning Solutions Ltd, Intel Corporation.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Unittests for provisioning module.
"""

__author__ = 'tmetsch'

from sdk.mcn import provisioning

import os
import unittest


class AbstractMethodTest(unittest.TestCase):
    """
    Test Abstract class.
    """

    def test_for_failure(self):
        """
        Test for not implemented methods.
        """
        self.assertRaises(NotImplementedError,
                          provisioning.Provisioner().provision, None, None)


class SshProvisionerTest(unittest.TestCase):
    """
    Unittest for SSH provisioner.
    """

    def setUp(self):
        self.cut = provisioning.SshProvisioner()

    def test_provision_for_sanity(self):
        """
        Test a SSH call.
        """
        self.cut.provision('localhost', 'ls -l',
                           username=os.environ['SSH_TEST_USER'],
                           password=os.environ['SSH_TEST_PWD'])