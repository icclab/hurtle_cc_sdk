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
        cls.cut = util.get_dnsaas(cls.token, tenant_name=cls.tenant)
        # Uncoment to Bypass MaaS
        #cls.cut = util.get_dnsaas(cls.token, tenant_name=cls.tenant, maas_endpoint_address='130.92.70.207')


    @classmethod
    def tearDownClass(cls):
        """
        Dispose cut after test
        """
        util.dispose_dnsaas(cls.token, cls.cut)
        # sleep 10s to be gentle on the SM between post/delete
        time.sleep(10)

    def test0001_create_domain(self):
        domain_name = "test_dnsaas.com"
        email_name = "dnsaas_admin@onesource.pt"
        ttl = 3600
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_domain(domain_name, email_name, ttl, token)
        self.assertEqual(status, 1, msg = "ERROR Domain Created ")


    def test0002_create_domain2(self):
        domain_name = "test2_dnsaas.com"
        email_name = "dnsaas_admin@onesource.pt"
        ttl = 3600
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_domain(domain_name, email_name, ttl, token)
        self.assertEqual(status, 1, msg = "ERROR Domain Created")


    def test0003_create_domain3(self):
        domain_name = "test3_dnsaas.com"
        email_name = "dnsaas_admin@onesource.pt"
        ttl = 3600
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_domain(domain_name, email_name, ttl, token)
        self.assertEqual(status, 1, msg = "ERROR Domain Created ")


    def test0004_create_domain4(self):
        domain_name = "test4_dnsaas.com"
        email_name = "dnsaas_admin@onesource.pt"
        ttl = 3600
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_domain(domain_name, email_name,ttl, token)
        self.assertEqual(status, 1, msg = "ERROR domain Created ")


    def test0005_create_record_A1(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "192.168.1.1"
        type = "A"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating A record ")

    def test0006_get_record_A1(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "192.168.1.1"
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

    def test0007_update_record_A1_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "192.168.1.20"
        type = "A"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update A record ")

    def test0008_update_record_A1_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = 9200
        type = "A"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update A record ")

    def test0009_update_record_A1_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "This is a A record description changed"
        type = "A"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update A record ")

    def test0010_zdelete_record_A1(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        type = "A"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete A record ")


    def test0011_create_record_MX(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = "192.168.1.1"
        type = "MX"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token, priority = 10)
        self.assertEqual(status, 1, msg = "ERROR Creating MX record ")

    def test0012_get_record_MX(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        type = "MX"
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
        self.assertEqual(status, 1, msg="ERROR get MX record ")

    def test0013_update_record_MX_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        type = "MX"
        rec_data = 600
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update MX record ")

    def test0014_update_record_MX_priority(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = 100
        type = "MX"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'priority', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update MX record ")

    def test0015_update_record_MX_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = "This is a MX record description changed"
        type = "MX"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update MX record ")

    def test0016_zdelete_record_MX(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        type = "MX"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete MX record ")


    def test0017_create_record_AAAA(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "aaaa"
        rec_data = "2001:db8:0:1234:0:5678:9:12"
        type = "AAAA"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating AAAA record ")

    def test0018_get_record_AAAA(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "aaaa"
        rec_data = "2001:db8:0:1234:0:5678:9:12"
        type = "AAAA"
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
        self.assertEqual(status, 1, msg = "ERROR get AAAA record ")

    def test0019_update_record_AAAA_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "aaaa"
        rec_data = "2001:db8:0:1234:0:5678:9:12"
        type = "AAAA"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update AAAA record ")

    def test0020_update_record_AAAA_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "aaaa"
        rec_data = 9800
        type = "AAAA"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update AAAA record ")

    def test0021_update_record_AAAA_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "aaaa"
        rec_data = "This is a changed AAA record description"
        type = "AAAA"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update AAAA record ")

    def test0022_zdelete_record_AAAA(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "aaaa"
        type = "AAAA"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete AAAA record ")


    def test0023_create_record_CNAME(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "cname"
        rec_data = "mail.test4_dnsaas.com"
        type = "CNAME"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating CNAME record ")

    def test0024_get_record_CNAME(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "cname"
        type = "CNAME"
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
        self.assertEqual(status, 1, msg = "ERROR Creating CNAME record ")

    def test0025_update_record_CNAME_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "cname"
        rec_data = "mail56"
        type = "CNAME"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update CNAME record ")

    def test0026_update_record_CNAME_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "cname"
        rec_data = 9800
        type = "CNAME"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update CNAME record ")


    def test0027_update_record_CNAME_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "cname"
        rec_data = "This is a CNAME record changed description"
        type = "CNAME"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update CNAME record ")

    def test0028_zdelete_record_CNAME(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "cname"
        type = "CNAME"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete CNAME record ")


    def test0029_create_record_TXT(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "txt"
        rec_data = "This a text records, use for SPF...."
        type = "TXT"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating TXT record ")

    def test0030_get_record_TXT(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "txt"
        type = "TXT"
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
        self.assertEqual(status, 1, msg = "ERROR get TXT record ")

    def test0031_update_record_TXT_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "txt"
        rec_data = "This a text records, use for NAPTR...."
        type = "TXT"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating TXT record ")


    def test0032_update_record_TXT_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "txt"
        rec_data = 9500
        type = "TXT"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating TXT record ")


    def test0033_update_record_TXT_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "txt"
        rec_data = "This is a TXT record description changed"
        type = "TXT"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating TXT record ")

    def test0034_zdelete_record_TXT(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "txt"
        type = "TXT"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete TXT record ")


    def test0035_create_record_SRV(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        rec_data = "0 5060 sip.test4_dnsaas.com"
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token, priority = 40)
        self.assertEqual(status, 1, msg = "ERROR Creating SRV record ")

    def test0036_get_record_SRV(self):
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
        self.assertNotEqual(status, 0, msg = "ERROR get SRV record ")

    def test0037_update_record_SRV_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        rec_data = "0 4060 sip"
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertNotEqual(status, 0, msg = "ERROR get SRV record ")

    def test0038_update_record_SRV_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        rec_data = 6200
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertNotEqual(status, 0, msg = "ERROR get SRV record ")

    def test0039_update_record_SRV_priority(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        rec_data = 60
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'priority', rec_data, token)
        self.assertNotEqual(status, 0, msg = "ERROR get SRV record ")

    def test0040_update_record_SRV_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        rec_data = "This is a SRV record description changed"
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertNotEqual(status, 0, msg = "ERROR get SRV record ")

    def test0041_zdelete_record_SRV(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_sip._tcp"
        type = "SRV"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR Creating SRV record ")

    def test0042_create_record_NS(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = "ns4"
        type = "NS"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating NS record ")

    def test0043_get_record_NS(self):
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

    def test0044_update_record_NS_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = "ns6.otherdomain.com"
        type = "NS"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Updating NS record ")

    def test0045_update_record_NS_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = 9800
        type = "NS"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Updating NS record ")

    def test0046_update_record_NS_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        rec_data = "This is a changed NS description"
        type = "NS"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Updating NS record ")

    def test0047_zdelete_record_NS(self):
        domain_name = "test4_dnsaas.com"
        rec_name = ""
        type = "NS"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR Creating NS record ")

    def test0048_create_zone_PTR(self):
        domain_name = "4.168.192.in-addr.arpa"
        email_name = "dnsaas_admin@onesource.pt"
        ttl = 3600
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_domain(domain_name, email_name, ttl, token)
        self.assertEqual(status, 1, msg = "ERROR Domain Created ")

    def test0049_create_record_PTR(self):
        domain_name = "4.168.192.in-addr.arpa"
        rec_name = "www.domain2.com"
        rec_data = "1.4.168.192.in-addr.arpa"
        type = "PTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating PTR record ")

    def test0050_get_record_PTR(self):
        domain_name = "4.168.192.in-addr.arpa"
        rec_name = "1.4.168.192.in-addr.arpa"
        type = "PTR"
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
        self.assertEqual(status, 1, msg = "ERROR get PTR record ")

    def test0051_update_record_PTR_data(self):
        domain_name = "4.168.192.in-addr.arpa"
        rec_name = "1.4.168.192.in-addr.arpa"
        rec_data = "mail.domain1.com"
        type = "PTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating PTR record ")


    def test0052_update_record_PTR_ttl(self):
        domain_name = "4.168.192.in-addr.arpa"
        rec_name = "1.4.168.192.in-addr.arpa"
        rec_data = 9200
        type = "PTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating PTR record ")

    def test0053_update_record_PTR_description(self):
        domain_name = "4.168.192.in-addr.arpa"
        rec_name = "1.4.168.192.in-addr.arpa"
        rec_data = "This is a PTR description changed"
        type = "PTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating PTR record ")

    def test0054_zdelete_record_PTR(self):
        domain_name = "4.168.192.in-addr.arpa"
        rec_name = "1.4.168.192.in-addr.arpa"
        type = "PTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR Creating PTR record ")

    def test0055_create_zone_PTR(self):
         domain_name = "4.168.192.in-addr.arpa"
         token = os.environ['OS_AUTH_TOKEN']
         status = self.cut.delete_domain(domain_name, token)
         self.assertEqual(status, 1, msg = "ERROR delete Domain")

    def test0056_create_record_SPF(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "test4_dnsaas.com."
        rec_data = "v=spf1 +mx a:colo.example.com/28 -all"
        type = "SPF"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating SPF record ")

    def test0057_get_record_SPF(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "test4_dnsaas.com"
        type = "SPF"
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
        self.assertEqual(status, 1, msg = "ERROR get SPF record ")

    def test0058_update_record_SPF_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "test4_dnsaas.com"
        rec_data = "v=spf55 +mx a:colo.example.com/28 -all"
        type = "SPF"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating SPF record ")

    def test0059_update_record_SPF_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "test4_dnsaas.com."
        rec_data = 9800
        type = "SPF"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating SPF record ")

    def test0060_update_record_SPF_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "test4_dnsaas.com"
        rec_data = "This is a changed SPF record"
        type = "SPF"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating SPF record ")

    def test0061_zdelete_record_SPF(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "test4_dnsaas.com"
        type = "SPF"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete SPF record ")

    def test0062_create_record_SSHFP(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "2 1 6c3c958af43d953f91f40e0d84157f4fe7b4a898"
        type = "SSHFP"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating SSHFP record ")

    def test0063_get_record_SSHFP(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        type = "SSHFP"
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
        self.assertEqual(status, 1, msg = "ERROR get SSHFP record ")

    def test0064_update_record_SSHFP_data(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "1 1 6c3c958af43d953f91f40e0d84157f4fe7b4a898"
        type = "SSHFP"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Updating SSHFP record ")

    def test0065_update_record_SSHFP_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = 9200
        type = "SSHFP"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Updating SSHFP record ")

    def test0066_update_record_SSHFP_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        rec_data = "This is a changed SSHFP record description"
        type = "SSHFP"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Updating SSHFP record ")

    def test0067_zdelete_record_SSHFP(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "www"
        type = "SSHFP"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete SSHFP record ")


    def test0068_create_record_NAPTR(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_rfs787ec.cp"
        rec_data = "100 50 \"s\" \"za\" \"\" ."
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.create_record(domain_name, rec_name, type, rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR Creating NAPTR record ")

    def test0069_get_record_NAPTR(self):
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

    def test0070_update_record_NAPTR_data(self):
        domain_name = 'test4_dnsaas.com'
        rec_name = '_rfs787ec.cp'
        rec_data = "200 50 \"s\" \"za\" \"\" ."
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'data', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update NAPTR record ")

    def test0071_update_record_NAPTR_ttl(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_rfs787ec.cp"
        rec_data = 9800
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'ttl', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update NAPTR record ")

    def test0072_update_record_NAPTR_priority(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_rfs787ec.cp"
        rec_data = 60
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'priority', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update NAPTR record ")

    def test0073_update_record_NAPTR_description(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_rfs787ec.cp"
        rec_data = "This is a changed NAPTR description"
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_record(domain_name, rec_name, type, 'description', rec_data, token)
        self.assertEqual(status, 1, msg = "ERROR update NAPTR record ")

    def test0074_zdelete_record_NAPTR(self):
        domain_name = "test4_dnsaas.com"
        rec_name = "_rfs787ec.cp"
        type = "NAPTR"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_record(domain_name, rec_name, type, token)
        self.assertEqual(status, 1, msg = "ERROR delete NAPTR record ")


    def test0075_get_domain2(self):
        domain_name = "test2_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.get_domain(domain_name, token)
        try:
            if status['code'] >= 400:
                status = 0
            else:
                status = 1
        except:
            status = 1
            pass
        self.assertEqual(status, 1, msg = "ERROR Get domain ")


    def test0076_cupdate_domain_ttl(self):
        domain_name = "test_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_domain(domain_name, 'ttl', 3600, token)
        self.assertEqual(status, 1, msg = "failed to update  domain ttl Updated ")


    def test0077_cupdate_domain_email(self):
        domain_name = "test_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_domain(domain_name, 'email', 'admin_update@onesource.pt', token)
        self.assertEqual(status, 1, msg = "failed to update  domain email Updated ")


    def test0078_cupdate_domain_description(self):
        domain_name = "test_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.update_domain(domain_name, 'description', 'domain updated', token)
        self.assertEqual(status, 1, msg = "failed to update domain description Updated ")


    def test0079_get_domain1(self):
        domain_name = "test_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.get_domain(domain_name, token)
        try:
            if status['code'] >= 400:
                status = 0
            else:
                status = 1
        except:
            status = 1
            pass
        self.assertEqual(status, 1, msg = "ERROR Get Domain")


    def test0080_delete_domain1(self):
        domain_name = "test_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_domain(domain_name, token)
        self.assertEqual(status, 1, msg = "ERROR delete Domain")

    def test0081_delete_domain2(self):
        domain_name = "test2_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_domain(domain_name, token)
        self.assertEqual(status, 1, msg = "ERROR delete Domain")

    def test0082_delete_domain3(self):
        domain_name = "test3_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_domain(domain_name, token)
        self.assertEqual(status, 1, msg = "ERROR delete Domain")



    def test0083_create_geo_map(self):
        token = os.environ['OS_AUTH_TOKEN']
        recordName = 'video'
        domainName = 'test4_dnsaas.com'
        geoInfo = ['124 IP.Canada.com.','250 France','276 GermanyYoutube','344 Hong-Kong','528 Netherlands','642 Romania','0 default.youtube.com.']
        status = self.cut.create_geo_map(recordName,domainName,geoInfo,token)
        self.assertEqual(status, 1, msg = "ERROR Geo Map already exists ")

        #####
        ##### GEO DNS TESTING

    def test0084_get_geo_map(self):
        token = os.environ['OS_AUTH_TOKEN']
        recordName = 'video'
        domainName = 'test4_dnsaas.com'
        status = self.cut.get_geo_map(recordName, domainName, token)
        try:
            if status['code'] >= 400:
                status = 0
            else:
                status = 1
        except:
            status = 1
            pass
        self.assertEqual(status, 1, msg = "Map does not exist ")

    def test0085_append_geo_map(self):
        token = os.environ['OS_AUTH_TOKEN']
        recordName = 'video'
        domainName = 'test4_dnsaas.com'
        dataToAppend = ['200 usa','300 UK']
        status = self.cut.append_geo_map(recordName,domainName,dataToAppend,token)
        self.assertEqual(status, 1, msg = "Map does not exist ")

    def test0086_delete_item_geo_map(self):
        token = os.environ['OS_AUTH_TOKEN']
        recordName = 'video'
        domainName = 'test4_dnsaas.com'
        infoToRemove = ['344 Hong-Kong','528 Netherlands']
        status = self.cut.delete_geo_map(recordName, domainName,token,infoToRemove=infoToRemove)
        self.assertEqual(status, 1, msg = "Map does not exist ")

    def test0087_delete_geo_map(self):
        token = os.environ['OS_AUTH_TOKEN']
        recordName = 'video'
        domainName = 'test4_dnsaas.com'
        status = self.cut.delete_geo_map(recordName, domainName,token)
        self.assertEqual(status, 1, msg = "Map does not exist ")

    def test0088_delete_domain4(self):
        domain_name = "test4_dnsaas.com"
        token = os.environ['OS_AUTH_TOKEN']
        status = self.cut.delete_domain(domain_name, token)
        self.assertEqual(status, 1, msg = "ERROR delete Domain")




if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()