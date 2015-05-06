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

import unittest
import os

from sdk.mcn import security

from keystoneclient.v2_0 import client


class AuthServiceTest(unittest.TestCase):
    """
    Tests auth services.
    """

    def setUp(self):
        self.cut = security.AuthService(None)

    def test_for_failure(self):
        """
        Tests signatures and not implemented errors.
        """
        self.assertRaises(NotImplementedError, self.cut.verify, None)


class SystemTest(unittest.TestCase):
    """
    Testing with Keystone.
    """

    def setUp(self):        # setup
        if 'OS_USER' not in os.environ or 'OS_PWD' not in os.environ:
            raise AttributeError('Please provide OS_USER, OS_PWD as env vars.')
        if 'DESIGN_URI' in os.environ:
            kep = os.environ['DESIGN_URI']
        else:
            kep = 'http://localhost:35357/v2.0'

        user = os.environ['OS_USER']
        pwd = os.environ['OS_PWD']
        if 'OS_TENANT' in os.environ:
            t_name = os.environ['OS_TENANT']
        else:
            t_name = 'demo'

        # keystone stuff.
        keystone = client.Client(username=user,
                                 password=pwd,
                                 tenant_name=t_name,
                                 auth_url=kep)
        self.token = keystone.auth_token
        self.cut = security.KeyStoneAuthService(kep)

    def test_verify_for_sanity(self):
        """
        Verify a valid and none valid token.
        """
        self.assertFalse(self.cut.verify('foobar'))
        self.assertTrue(self.cut.verify(self.token))


