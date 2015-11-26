## Cloud Controller SDK

### Function
The SDK is a library containing many helper functions for service orchestrators to create and manage their services. A main function of the SDK in the current implementation is to deploy Heat templates on an underlying infrastructure, but it also offers many more methods.

### Local Installation

The CC SDK is provided with a setup script.

    python setup.py install
  
### Helper methods
Below is a short description of the main functions in each component of the CC SDK. Details on each method provided by these components are provided within the inline documentation.
#### sdk.services
This class provides service discovery methods to retrieve service endpoint for a given service type within the service registry.
#### sdk.mcn.security
This class provides authentication methods to be used by other classes of the SDK. The current implementation is restricted to Keystone authentication.
#### sdk.mcn.runtime
The runtime library offers functions to be used by service orchestrators to create and manage alarms and callback notifications for runtime management of their service. More information can be found in the runtime_usage.md document.
#### sdk.mcn.deployment
This file contains an interface for generic deployers with one implementation for deployment via Heat. It provides methods to CRUD Heat templates through a user provided Heat endpoint.
#### sdk.mcn.util
Util provides static methods to retrieve instances of a deployer object, of the auth object, as well as method to create or dispose automatically instances of some atomic services. Note that using these methods circumvent the normal usage of the service graph and the resolver which are normally tasked to deploy all services comprising a composed application.

### Usage Examples
Examples of using the SDK are provided within the sample_so repository, below the most typical use case for the SDK: managing heat templates.

    token = '123213' # Keystone token
    tenant = 'demo' # Openstack tenant
    template = '...' # Heat template as a string
    # Deployer object
    deployer = util.get_deployer(token,
                                 url_type='public',
                                 tenant_name=tenant)
    # Deploy a template                              
    stack_id = deployer.deploy(template, token)
    # Get a stack details
    details = deployer.details(stack_id, token)
    # Update a stack
    deployer.update(template, token)    
    # Destroy a stack
    deployer.dispose(stack_id, token)

## Supported by

<div align="center" >
<a href='http://blog.zhaw.ch/icclab'>
<img src="https://raw.githubusercontent.com/icclab/hurtle/master/docs/figs/mcn_logo.png" title="mobile cloud networking" width=400px>
</a>
</div>
