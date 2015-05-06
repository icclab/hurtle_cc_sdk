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


import os
import unittest
import logging

from keystoneclient.v2_0 import client

from sdk.mcn import deployment
from sdk.mcn import provisioning
from sdk.mcn import security
from sdk.mcn import util

LOG = logging.getLogger()


class SystemTest(unittest.TestCase):
    """
    Test for utility functions.
    """

    def setUp(self):
        # setup
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
        keystone = client.Client(username=user,
                                 password=pwd,
                                 tenant_name=t_name,
                                 auth_url=kep)
        self.token = keystone.auth_token

    def test_retrieval_for_failure(self):
        """
        Test retrieval.
        """
        self.assertIsNone(util.get_deployer(self.token, 'aws'))
        self.assertIsNone(util.get_security_service(self.token, 'LDAP'))

    def test_get_deployer_for_success(self):
        """
        Test retrieval of Deployer for success.
        """
        tmp = util.get_deployer(self.token)

        self.assertTrue(isinstance(tmp, deployment.Deployer))

    def test_get_provsioning_for_success(self):
        """
        Test retrieval of Provisioning for success.
        """
        tmp = util.get_provisioner(self.token)

        self.assertTrue(isinstance(tmp, provisioning.SshProvisioner))

    def test_get_security_for_success(self):
        """
        Test retrieval of security service.
        """
        tmp = util.get_security_service(self.token)

        self.assertTrue(isinstance(tmp, security.KeyStoneAuthService))

    def test_get_maas_for_success(self):
        """
        Test retrieval of maas.
        """
        tmp = util.get_maas(self.token)

    def test_get_deployer_for_sanity(self):
        """
        Test retrieval of Deployer for sanity with regions in place.

        Requires:

        keystone service-create
            --name=cs_heat
            --type=orchestration
            --description="A CS heat service"

        keystone endpoint-create
            --region CloudSigma --service-id=<id>
            --publicurl=http://192.168.206.130:5000/v2.0
            --internalurl=http://192.168.206.130:5000/v2.0
            --adminurl=http://192.168.206.130:35357/v2.0
        """
        tmp0 = util.get_deployer(self.token)
        self.assertTrue(tmp0.endpoint.find('http://192.168.0.181:8004') != -1)

        tmp1 = util.get_deployer(self.token, region='CloudSigma')
        if tmp1 is not None:
            LOG.warn('Could not find CloudSigma region.')
            self.assertTrue(tmp1.endpoint.find('http://192.168.206.130:5000')
                            != -1)

        tmp2 = util.get_deployer(self.token, region='Antartica')
        self.assertIsNone(tmp2)
