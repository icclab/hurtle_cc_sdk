# Copyright 2014 Copyright (c) 2013-2015, OneSource, Portugal.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

__author__ = 'Claudio Marques / Bruno Sousa - OneSource'
__copyright__ = "Copyright (c) 2013-2015, Mobile Cloud Networking (MCN) project"
__credits__ = ["Claudio Marques - Bruno Sousa"]
__license__ = "Apache"
__version__ = "1.0"
__maintainer__ = "Claudio Marques - Bruno Sousa"
__email__ = "claudio@onesource.pt, bmsousa@onesource.pt"
__status__ = "Production"

import unittest
import os
import time

from keystoneclient.v2_0 import client

from sdk.mcn import util


try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class DNSaaS_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Instantiate a fresh DNSaaS object before every test
        """
        # checking vor credentials
        if 'OS_USERNAME' not in os.environ or 'OS_PASSWORD' not in os.environ:
            raise AttributeError('Please provide OS_USERNAME, OS_PASSWORD as env vars.')
        if 'DESIGN_URI' in os.environ:
            kep = os.environ['DESIGN_URI']
        else:
            kep = 'http://localhost:35357/v2.0'

        user = os.environ['OS_USERNAME']
        pwd = os.environ['OS_PASSWORD']

        # retrieve token for later usage
        if 'OS_TENANT_NAME' in os.environ:
            cls.tenant = os.environ['OS_TENANT_NAME']
        else:
            cls.tenant = 'mcn-dns'

        keystone = client.Client(username=user, password=pwd,
                                 tenant_name=cls.tenant, auth_url=kep)
        cls.token = keystone.auth_token

        # instantiate class under test.
        #cls.cut = util.get_dnsaas(cls.token, tenant_name=cls.tenant, mcn_endpoint_api='130.92.70.245')

        cls.cut = util.get_dnsaas(cls.token, tenant_name=cls.tenant)



    # @classmethod
    # def tearDownClass(cls):
    #    """
    #    Dispose cut after test
    #    """
    #    util.dispose_dnsaas(cls.token, cls.cut)
    #    #sleep 10s to be gentle on the SM between post/delete
    #    time.sleep(10)

    def test0001_create_domain(self):
        domain_name = "test4_dnsaas.com"
        email_name = "dnsaas_admin@onesource.pt"
        ttl = 3600
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_domain(domain_name, email_name, ttl, token)
        self.assertEqual(status, 1, msg = "ERROR Domain Created ")


    def test0002_create_record_A1(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "192.168.1.1"
        type = "A"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating A record ")

    def test0003_get_record_A1(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        type = "A"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.get_record(domain_name, rec_name, type, token)
        try:
            if status['code'] >= 400:
                status = 0
            else:
                status = 1
        except:
            status = 1
            pass
        self.assertEqual(status, 1, msg = "ERROR Creating A record ")

    def test0004_create_record_SRV(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        rec_data = "0 5060 sip.test4_dnsaas.com"
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token, priority = 40)
        self.assertEqual(status, 1, msg = "ERROR Creating SRV record ")

    def test0005_get_record_SRV(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.get_record(domain_name, rec_name, type, token)
        try:
            if status['code'] >= 400:
                status = 0
            else:
                status = 1
        except:
            status = 1
            pass
        self.assertEqual(status, 1, msg = "ERROR get SRV record ")

    def test0006_create_record_NS(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = "ns4"
        type = "NS"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating NS record ")

    def test0007_get_record_NS(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        type = "NS"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.get_record(domain_name, rec_name, type, token)
        try:
            if status['code'] >= 400:
                status = 0
            else:
                status = 1
        except:
            status = 1
            pass
        self.assertEqual(status, 1, msg = "ERROR get NS record ")

    def test0008_create_record_NAPTR(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_rfs787ec.cp"
        rec_data = "100 50 \"s\" \"za\" \"\" ."
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating NAPTR record ")

    def test0009_get_record_NAPTR(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_rfs787ec.cp"
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.get_record(domain_name, rec_name, type, token)
        try:
            if status['code'] >= 400:
                status = 0
            else:
                status = 1
        except:
            status = 1
            pass
        self.assertEqual(status, 1, msg = "ERROR get NAPTR record ")


    def test0010_delete_domain1(self):
        domain_name = "test4_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_domain(domain_name, token)
        self.assertEqual(status, 1, msg = "ERROR delete Domain")


if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()
