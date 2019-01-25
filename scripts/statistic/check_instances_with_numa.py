import os
import sys

from oslo_log import log as logging
from nova import config
from nova import objects
from nova import context
from nova.virt import hardware
import nova.conf

CONF = nova.conf.CONF
LOG = logging.getLogger('instance_numa_check')


RETURN_IP_LIST = False


def check_instance_numa(instance):
    flavor = instance.flavor
    numa_topology = hardware.numa_get_constraints(flavor, instance.image_meta)
    if numa_topology:
        return True
    return False


def get_cn_ip(instance):
    host = instance.host
    # e.g. 'yn01-compute-10e106e5e108'
    return host.split('-')[2].replace('e', '.')


def get_inst_ip(instance):
    # simple return because each instance has single nic
    return instance.get_network_info()[0]['network']['subnets'][0]['ips'][0]['address']
    # inst_ip_addr = []
    # networks = instance.get_network_info()
    # for n in networks:
    #     subnets = n['network']['subnets']
    #     for s in subnets:
    #         ips = s['ips']
    #         for ip in ips:
    #             addr = ip['address']
    #             inst_ip_addr.append(addr)
    # return inst_ip_addr


if __name__ == '__main__':
    config.parse_args(sys.argv)
    logging.setup(CONF, 'instance')
    objects.register_all()

    cxt = context.get_admin_context()
    instances = objects.InstanceList.get_all(cxt)
    inst_with_numa = []
    inst_without_numa = []
    for instance in instances:
        ret = check_instance_numa(instance)
        cn_ip = get_cn_ip(instance)
        inst_ip = get_inst_ip(instance) or ''
        ip_tuple = (cn_ip, inst_ip)
        if ret:
            inst_with_numa.append(ip_tuple)
        else:
            inst_without_numa.append(ip_tuple)

    print("Amount of instances with numa is %s" % len(inst_with_numa))
    print("Amount of instances without numa is %s" % len(inst_without_numa))

    with open('/root/instances_no_numa', 'w') as f:
        for cn_ip, inst_ip in inst_without_numa:
            f.write(cn_ip + "\t" + inst_ip + '\n')
    with open('/root/instances_with_numa', 'w') as f_2:
        for cn_ip, inst_ip in inst_with_numa:
            f_2.write(cn_ip + "\t" + inst_ip + '\n')
