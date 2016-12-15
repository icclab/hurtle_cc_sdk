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
Setuptools script.
"""

from setuptools import setup

setup(
    name='hurtle_cc_sdk',
    version='1.2.1',
    description='Service Development Kit',
    author='Intel Performance Learning Solutions Ltd, Intel Corporation.',
    author_email='thijs.metsch@intel.com',
    url='http://www.intel.com',
    license='Apache 2.0',
    packages=['sdk', 'sdk.mcn'],
    install_requires=['paramiko',
                      'pyssf',
                      'python-heatclient',
                      'python-keystoneclient',
                      'zabbix-api>=0.4',
                      'requests']
)
