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
import time
import unittest

from sdk.mcn import deployment
from sdk.mcn import util

from keystoneclient.v2_0 import client


class DeploymentTest(unittest.TestCase):
    """
    Tests deployment services.
    """

    def setUp(self):
        self.cut = deployment.Deployer(None)

    def test_for_failure(self):
        """
        Tests signatures and not implemented errors.
        """
        self.assertRaises(NotImplementedError, self.cut.dispose, None, None)
        self.assertRaises(NotImplementedError, self.cut.deploy, None, None)
        self.assertRaises(NotImplementedError, self.cut.details, None, None)
        self.assertRaises(NotImplementedError, self.cut.get_template, None,
                          None)
        self.assertRaises(NotImplementedError, self.cut.update, None, None,
                          None)
        self.assertRaises(NotImplementedError, self.cut.check_output, None,
                          None, None)


class SystemTest(unittest.TestCase):
    """
    System test with running heat.
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

        # keystone stuff.
        keystone = client.Client(username=user,
                                 password=pwd,
                                 tenant_name=t_name,
                                 auth_url=kep)
        self.token = keystone.auth_token

        # class under test
        self.cut = util.get_deployer(self.token)

    def test_deploy_for_sanity(self):
        """
        Test deployment of wordpress.
        """
        template = _read_template('wordpress.yaml')

        tmp = self.cut.deploy(template,
                              self.token,
                              name='foo')
        self.assertIsNotNone(tmp)

        # wait for stack to be deployed
        self._wait_for_state(tmp, 'CREATE_COMPLETE')
        tmp2 = self.cut.details(tmp, self.token)

        self.assertTrue(isinstance(tmp2, dict))
        self.assertTrue(tmp2['output'][0]['output_key'] == 'WebsiteURL')
        self.assertEquals(tmp2['state'], 'CREATE_COMPLETE')

        self.cut.dispose(tmp, self.token)

    def test_deploy_with_parameters_for_sanity(self):
        """
        Tests ops on parameters.
        """
        template = _read_template('input_output.yaml')

        iden = self.cut.deploy(template, self.token,
                               parameters={'ParaOne': 'foo'})
        time.sleep(2)
        self.assertEquals(self.cut.check_output('OutputOne', iden, self.token),
                          'foo')
        self.assertEquals(self.cut.check_output('OutputTwo', iden, self.token),
                          ['foo', 'bar'])

        self.cut.dispose(iden, self.token)

    def test_update_for_sanity(self):
        """
        Test updating a stack.
        """
        template = _read_template('simple_vm.yaml')
        iden = self.cut.deploy(template, self.token,
                               parameters={'InstanceType': 'm1.nano'})

        # wait for stack to be up
        self._wait_for_state(iden, 'CREATE_COMPLETE')

        # now let's update with new parameter
        self.cut.update(iden, template, self.token,
                        parameters={'InstanceType': 'm1.micro'})
        self._wait_for_state(iden, 'UPDATE_COMPLETE')
        tmp = self.cut.details(iden, self.token)
        self.assertTrue(tmp['output'][0]['output_key'] == 'VMOneIP')

        # now let's change complete template
        new_template = _read_template('twomachine.yaml')
        self.cut.update(iden, new_template, self.token)
        self._wait_for_state(iden, 'UPDATE_COMPLETE')

        tmp = self.cut.details(iden, self.token)
        self.assertTrue(tmp['output'][0]['output_key'] == 'ExternalIp')

        self.cut.dispose(iden, self.token)

    def test_update_without_replace(self):
        temp1 = '''
heat_template_version: 2013-05-23
resources:
  server1:
    type: OS::Nova::Server
    properties:
      name: Server1
      image: cirros-0.3.2-x86_64-disk
      flavor: m1.nano
outputs:
  server1_iden:
    value: { get_attr: [ server1, instance_name ] }
    description: Id of VM.
        '''
        temp3 = '''
heat_template_version: 2013-05-23
resources:
  server2:
    type: OS::Nova::Server
    properties:
      name: Server2
      image: cirros-0.3.2-x86_64-disk
      flavor: m1.micro
outputs:
  server2_iden:
    value: { get_attr: [ server2, instance_name ] }
    description: Id of VM.
        '''
        temp2 = temp1.replace('flavor: m1.nano', 'flavor: m1.micro')
        self.assertNotEquals(temp1, temp2)

        # deploy stack
        iden = self.cut.deploy(temp1, self.token, name='bar')
        self._wait_for_state(iden, 'CREATE_COMPLETE')
        tmp = self.cut.details(iden, self.token)
        iden_a = tmp['output'][0]['output_value']

        # update a VM - NO Replace expected.
        self.cut.update(iden, temp2, self.token)
        self._wait_for_state(iden, 'UPDATE_COMPLETE')
        tmp = self.cut.details(iden, self.token)
        iden_b = tmp['output'][0]['output_value']

        self.assertEquals(iden_b, iden_a)

        # update complete stack - replace expected
        self.cut.update(iden, temp3, self.token)
        self._wait_for_state(iden, 'UPDATE_COMPLETE')
        tmp = self.cut.details(iden, self.token)
        iden_c = tmp['output'][0]['output_value']

        self.assertNotEquals(iden_a, iden_c)

        # cleanup
        self.cut.dispose(iden, self.token)

    def test_get_template_for_sanity(self):
        """
        Deploy a simple stack and return the template from heat in YAML format.
        """
        template = _read_template('simple_vm.yaml')
        iden = self.cut.deploy(template, self.token,
                               parameters={'InstanceType': 'm1.nano'})

        # wait for stack to be up
        self._wait_for_state(iden, 'CREATE_COMPLETE')

        # retrieve the template
        tmp = self.cut.get_template(iden, self.token)

        self.assertIn('InstanceType', tmp['Parameters'])

        # cleanup
        self.cut.dispose(iden, self.token)

    def _wait_for_state(self, iden, status):
        """
        Wait for a stack to read certain state..
        """
        i = 0
        state = ''
        while state != status:
            time.sleep(10)
            tmp2 = self.cut.details(iden, self.token)
            state = tmp2['state']
            i += 1
            if i > 10:
                self.assertTrue(False, "Stack not in desired state!")


class FreakingHeatTest(unittest.TestCase):
    """
    OpenStack Juno's heat version misbehaves. Esp on software config
    resources.

    This issue does not happen with a vanilla openstack juno:

    heat==2015.1.dev309
    python-heatclient==0.2.12

    Only affected sys for now is Zhaw testbed installed with Fuel. So I'm
    suspect it is the fuel release atm.

    This can be fixed by providing a username and password arguments to the
    heat client. Now the weird part: password is NOT actual the password but a
    token.
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

        # keystone stuff.
        keystone = client.Client(username=user,
                                 password=pwd,
                                 tenant_name=t_name,
                                 auth_url=kep)
        self.token = keystone.auth_token

        # class under test
        self.cut = util.get_deployer(self.token)

    def test_deploy_for_sanity(self):
        """
        Test deployment of a stack with software config resources.
        """
        template = _read_template('soft_config.yaml')
        stack_id = self.cut.deploy(template,
                                   self.token,
                                   name='freaking_openstack_stack')

        self._wait_for_state(stack_id, 'CREATE_COMPLETE')

        self.cut.dispose(stack_id, self.token)

    def _wait_for_state(self, iden, status):
        """
        Wait for a stack to read certain state..
        """
        i = 0
        state = ''
        while state != status:
            time.sleep(10)
            tmp2 = self.cut.details(iden, self.token)
            state = tmp2['state']
            i += 1
            if i > 10:
                self.assertTrue(False, "Stack not in desired state!")


def _read_template(name):
    """
    Read template from file.
    """
    fn = os.path.join('tests', 'files', name)
    f = open(fn)
    template = f.read()
    f.close()
    return template
