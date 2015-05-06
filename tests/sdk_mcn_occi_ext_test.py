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

from sdk.mcn import occi_ext

from occi import core_model

import unittest


class ApplicationTest(unittest.TestCase):
    """
    Test the application class.
    """

    def test_init_for_success(self):
        occi_ext.Application(_MyBackend())
        occi_ext.Application(_MyBackend(),
                             backends={core_model.Kind('foo',
                                                       'bar'):
                                           _MyBackend()})

    def test_call_for_success(self):
        app = occi_ext.Application(_MyBackend())
        wsgi = {'HTTP_X_AUTH_TOKEN': '123',
                'HTTP_X_TENANT_NAME': 'demo',
                'SERVER_NAME': 'machine1',
                'SERVER_PORT': '8080',
                'PATH_INFO': '/',
                'REQUEST_METHOD': 'GET',
                'wsgi.url_scheme': 'https'}
        app.__call__(wsgi, _DummyResponse())

    def test_call_for_failure(self):
        app = occi_ext.Application(_MyBackend())
        wsgi = {'SERVER_NAME': 'machine1',
                'SERVER_PORT': '8080',
                'PATH_INFO': '/',
                'REQUEST_METHOD': 'GET',
                'wsgi.url_scheme': 'https'}
        self.assertEquals(app.__call__(wsgi, _DummyResponse()),
                          'X-Auth-Token required...')
        wsgi = {'SERVER_NAME': 'machine1',
                'SERVER_PORT': '8080',
                'PATH_INFO': '/',
                'REQUEST_METHOD': 'GET',
                'wsgi.url_scheme': 'https',
                'HTTP_X_AUTH_TOKEN': 'foobar'}
        self.assertEquals(app.__call__(wsgi, _DummyResponse()),
                          'X-Tenant-Name required...')


class BackendTest(unittest.TestCase):
    """
    Tests generic backend.
    """

    def setUp(self):
        self.res = core_model.Resource('/foo/123', occi_ext.ORCHESTRATOR, [])

    def test_for_failure(self):
        self.assertRaises(NotImplementedError, occi_ext.Backend().deploy_me,
                          None, None, None)
        self.assertRaises(NotImplementedError, occi_ext.Backend().provision_me,
                          None, None, None)

    def test_action_for_failure(self):
        back = _MyBackend()
        self.assertRaises(AttributeError, back.action, self.res,
                          occi_ext.PROVISION_ACTION, [], None)

    def test_action_for_sanity(self):
        self.res.actions = [occi_ext.DEPLOY_ACTION]
        back = _MyBackend()
        back.action(self.res, occi_ext.DEPLOY_ACTION, {}, None)
        back.action(self.res, occi_ext.PROVISION_ACTION, {}, None)
        self.assertTrue(len(self.res.actions) == 0)


class _MyBackend(occi_ext.Backend):
    """
    Dummy class.
    """

    def deploy_me(self, entity, attributes, extras):
        entity.actions = [occi_ext.PROVISION_ACTION]

    def provision_me(self, entity, attributes, extras):
        entity.actions = []


class _DummyResponse(object):
    """
    Dummy class.
    """

    def __call__(self, *args, **kwargs):
        pass