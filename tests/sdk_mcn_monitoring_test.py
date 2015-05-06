#   Copyright (c) 2014, Technische Universitaet Berlin
#   All Rights Reserved.
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

import time

import unittest

from keystoneclient.v2_0 import client

from sdk.mcn import util

from sdk.mcn import monitoring


class MonitoringTest(unittest.TestCase):
    """
    Test Monitoring part running Zabbix.
    """

    def setUp(self):
        """
        Instantiate a fresh MaaS object before every test
        """
        # checking vor credentials
        if 'OS_USER' not in os.environ or 'OS_PWD' not in os.environ:
            raise AttributeError('Please provide OS_USER, OS_PWD as env vars.')
        if 'DESIGN_URI' in os.environ:
            kep = os.environ['DESIGN_URI']
        else:
            kep = 'http://localhost:35357/v2.0'

        user = os.environ['OS_USER']
        pwd = os.environ['OS_PWD']

        # retrieve token for later usage
        if 'OS_TENANT' in os.environ:
            self.tenant = os.environ['OS_TENANT']
        else:
            self.tenant = 'mcntub'

        keystone = client.Client(username=user, password=pwd,
                                 tenant_name=self.tenant, auth_url=kep)
        self.token = keystone.auth_token

        # instantiate class under test.
        self.cut = util.get_maas(self.token, tenant_name=self.tenant)

    def tearDown(self):
        """
        Dispose cut after test
        """
        util.dispose_maas(self.token, self.cut)
        # sleep 10s to be gentle on the SM between post/delete
        time.sleep(10)

    def test_parentclass_for_sanity(self):
        """
        Test dummy parentclass method
        """
        self.parent_cut = monitoring.Monitoring()
        self.assertRaises(NotImplementedError,
                          self.parent_cut.get_address, None)
        self.assertRaises(NotImplementedError,
                          self.parent_cut.get_metric, None, None)
        # sleep 10s to be gentle on the SM between post/delete
        time.sleep(10)

    def test_get_metric_for_sanity(self):
        """
        Tests the retrieval of one metric value
        """
        # this needs to be executed to set the address correctly
        self.cut.get_address(self.token)
        # in case zabbix is not up and running yet, wait 30 more secs.
        time.sleep(30)
        # test with default credentials
        self.assertNotEqual(self.cut.get_metric("Zabbix Server",
                                                "Host local time"),
                            0, "Getitem failed!")

        # overwrite credentials
        self.assertNotEqual(self.cut.get_metric("Zabbix Server",
                                                "Host local time",
                                                password="zabbix",
                                                username="admin"),
                            0, "Getitem with kwargs failed!")
        # if the address is set to None, there will be no metric received
        self.cut.set_address(None)
        self.assertEqual(self.cut.get_metric("Zabbix Server",
                                             "Host local time"),
                         None, "Getitem without address failed!")

    def test_class_attributes(self):
        """
        Tests for correctly set class attributes when deploying two objects.
        """
        self.cut2 = util.get_maas(self.token, tenant_name=self.tenant)

        self.assertEqual(self.cut.get_address(self.token),
                         self.cut2.get_address(self.token),
                         "Class variable address not correctly set!")
        self.assertEquals(self.cut.get_location(), self.cut2.get_location(),
                          "Class variable location not correctly set!")
        self.assertEquals(self.cut.get_tenant(), self.cut2.get_tenant(),
                          "Class variable tenant not correctly set!")

    def test_attributes_for_sanity(self):
        """
        Test if all attributes are getting set correctly on deploy
        """
        self.assertNotEquals(self.cut.get_address(self.token), 0,
                             "Address not set!")
        self.assertEqual(self.cut.get_tenant(), self.tenant,
                         "Tenant not set!")
        self.assertNotEqual(self.cut.get_location(), 0,
                            "Location not set!")

        # if location somehow did not get set, address would fail on
        # run and thus will fallback to None
        tmp_location = self.cut.get_location()
        self.cut.set_location(None)
        self.assertEquals(self.cut.get_address(self.token), None,
                          "Fail on address without location!")
        # restore location, otherwise tearDown will fail
        self.cut.set_location(tmp_location)
