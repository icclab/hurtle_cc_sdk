# Notes

The files for the wordpress template are taken from: [heat-templates](https://github.com/openstack/heat-templates).

Requires a Fedora image. In devstack do:

    IMAGE_URLS="http://cloud-images.ubuntu.com/trusty/20140512/trusty-server-cloudimg-amd64-disk1.img,http://download.fedoraproject.org/pub/fedora/linux/updates/20/Images/x86_64/Fedora-x86_64-20-20140407-sda.qcow2,http://download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img"

Test LBaaS with Heat
====================

*rif. Luigi GROSSI (TI), 2014 MAR 13*

The yaml template file is *compute-net-lb.yaml* and the command used to deploy the stack is:

    $ heat stack-create mystack2 --template-file=/root/openstack/heat-templates/compute-net-lb.yaml --parameters="image=CirrOS;flavor=m1.small;private_net_name=private-net;private_net_cidr=10.70.70.0/24;private_net_gateway=10.70.70.1;private_net_pool_start=10.70.70.5;private_net_pool_end=10.70.70.253;lb_vip_address=10.70.70.4"

Three servers are instantiated: Server1, Server2, Server3

Server1 and Server2 are behind a http roundrobin load-balancer and Server3 is used to access them.

First attempts didn't succeed because no members were added to the pool and neither was possible to delete the created stack. The reason of this is a bug in heat (https://bugs.launchpad.net/heat/+bug/1247638).

Test of load-balancing functionality was performed through the following steps:

1. log in Server1 and edit and run a script to emulate a http server. This emulates a web server by answering with http OK to any message incoming on port 80.
When you launch it you will soon see echoed on the console the Http GET messages coming from the health monitor.

        $ vi Server1.sh
        while true
        do
        echo -e 'HTTP/1.0 200 OK\r\n\r\nServer1' | sudo nc -l -p 80
        done

2. do the same on Server2: make sure you also change to 'Server2' the server name in the http answer

3. on Server3 issue a http GET onto the load balancer VIP with:

        $ wget -O - http://10.70.70.4

You will see answers alternately coming from Server1 and Server2.