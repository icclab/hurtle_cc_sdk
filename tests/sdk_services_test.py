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

from keystoneclient.v2_0 import client
from keystoneclient.v2_0 import endpoints

from sdk import services


class SystemTest(unittest.TestCase):
    """
    Test with running keystone.
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

    # test for failure

    def test_retrieve_endpoint_for_failure(self):
        """
        Test for failure/None.
        """
        tmp = services.get_service_endpoint('foobar', self.token)
        self.assertIsNone(tmp)

        tmp = services.get_service_endpoint('heat', self.token,
                                            tenant_name='foo')
        self.assertIsNone(tmp)

    def test_get_url_type_for_failure(self):
        """
        Test for failure.
        """
        item = endpoints.Endpoint(None, {})
        self.assertRaises(AttributeError, services._get_url_type, item,
                          url_type='foobar')

    # test for sanity

    def test_service_listing_for_sanity(self):
        """
        Test listing of services for sanity.
        """
        tmp = services.list_services(self.token)
        self.assertTrue('heat' in tmp.keys())

    def test_retrieve_endpoint_for_sanity(self):
        """
        Test retrieval of endpoint for sanity.
        """
        tmp = services.get_service_endpoint('orchestration', self.token)
        self.assertIsNot(tmp.find(':8004/v1'), -1)

        tmp = services.get_service_endpoint('identity', self.token)
        self.assertIsNot(tmp.find(':5000/v2.0'), -1)

    def test_design_uri_injection(self):
        """
        Test if design uri can be set via environment variable.
        """
        if 'DESIGN_URI' in os.environ:
            return
        os.environ['DESIGN_URI'] = 'http://localhost:35357/v2.0'
        services.list_services(self.token)
        services.get_service_endpoint('heat', self.token)
        os.environ.pop('DESIGN_URI')

    def test_get_url_type_for_sanity(self):
        item = endpoints.Endpoint(None, {})
        item.publicurl = 'puburl'
        item.internalurl = 'int'

        # test default - should return internal
        endpoint = services._get_url_type(item)
        self.assertTrue(endpoint, 'int')

        # test specific - internal
        endpoint = services._get_url_type(item, url_type='internal')
        self.assertTrue(endpoint, 'int')

        # test specific - public
        endpoint = services._get_url_type(item, url_type='public')
        self.assertTrue(endpoint, 'puburl')
