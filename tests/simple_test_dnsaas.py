import os
import unittest
import time

from keystoneclient.v2_0 import client

from sdk.mcn import deployment
from sdk.mcn import security
from sdk.mcn import util
#from sdk.mcn.dnsaasclient import * 

if 'OS_USERNAME' not in os.environ or 'OS_PASSWORD' not in os.environ:
    raise AttributeError('Please provide OS_USER, OS_PWD as env vars.')
#if 'OS_AUTH_URL' in os.environ:
 #   kep = os.environ['OS_AUTH_URL']
#else:
    
kep = 'http://160.85.4.18:35357/v2.0'

user = os.environ['OS_USERNAME']
pwd = os.environ['OS_PASSWORD']
if 'OS_TENANT_NAME' in os.environ:
    t_name = os.environ['OS_TENANT_NAME']
else:
    t_name = 'demo'
keystone = client.Client(username=user,
                        password=pwd,
                        tenant_name=t_name,
                        auth_url=kep)
token = keystone.auth_token
#print token

ts = time.time()
dns=util.get_dnsaas(token, tenant_name=t_name, maas_endpoint_address="160.85.4.50")
#dns=util.get_dnsaas(token, tenant_name=t_name)

te = time.time()

print( "Time get_dnsaas= %3.5f" % (te-ts))

if dns is not None:
    time.sleep(10) # make sure dns is ready

    print dns.get_address()

    res = dns.create_domain('testdnsaas.com', 'test@testdnsaas.com.com', 3600, token)
    idDomain=dns.get_domain("testdnsaas.com", token)
    print idDomain

    dns.create_record('testdnsaas.com', 'www', 'A',  '192.168.1.4',token)
    print dns.get_record('testdnsaas.com', 'www', 'A', token)



    print("To dispose resources after some seconds....  ")
    time.sleep(360)

    #util.dispose_dnsaas(token, dns)