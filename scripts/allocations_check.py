# !/usr/bin/python
from prettytable import PrettyTable

from nova import compute
from nova import objects
from nova import servicegroup
from nova.context import RequestContext
import nova.scheduler.host_manager as host_manager
from nova.objects import resource_provider as rp_obj
from nova import config

import sys

color_tbl = {
    "grey": '\033[1;30m',
    "green": '\033[32m',
    "blue": '\033[34m',
    "yellow": '\033[33m',
    "red": '\033[31m',
}


def colorizer(num):
    if num <= 20:
        return "%s%.2f%%\033[0m" % (color_tbl['grey'], num)
    if num <= 40:
        return "%s%.2f%%\033[0m" % (color_tbl['green'], num)
    if num <= 60:
        return "%s%.2f%%\033[0m" % (color_tbl['blue'], num)
    if num <= 80:
        return "%s%.2f%%\033[0m" % (color_tbl['yellow'], num)
    return "%s%.2f%%\033[0m" % (color_tbl['red'], num)


config.parse_args(sys.argv)
cxt = RequestContext()
host_manager.objects.register_all()


def check_services():
    objects.register_all()
    host_api = compute.HostAPI()
    servicegroup_api = servicegroup.API()
    api_services = ('nova-osapi_compute', 'nova-ec2', 'nova-metadata')
    isOK = True
<<<<<<< HEAD
    print "======================= services check ======================="
=======
    print "============================ services check ============================"
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
    for s in host_api.service_get_all(cxt, set_zones=True, all_cells=True):
        if s['binary'] in api_services:
            continue
        if not servicegroup_api.service_is_up(s):
            isOK = False
            print "%s %s is down" % (s['host'], s['binary'])
        if s['disabled']:
            isOK = False
            print "%s %s is disabled" % (s['host'], s['binary'])
    if isOK:
        print "Service is OK"


def print_hypervisor_view():
    hm = host_manager.HostManager()
<<<<<<< HEAD
    tbl = PrettyTable(["hostname", "nodename", "updated", "ip", "cpu",
                       "cpu_ratio", "ram", "ram_ratio", "vms", "active_vms",
                       "other_vms"])
=======
    tbl = PrettyTable(["hostname", "nodename", "updated", "ip", "cpu", "cpu_ratio",
                       "ram", "ram_ratio", "vms", "active_vms", "other_vms"])
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
    tbl.align['hostname'] = 'l'
    tbl.align['ip'] = 'l'
    states = hm.get_all_host_states(cxt)
    for i in states:
        cpu = "%s/%s" % (i.vcpus_used, i.vcpus_total)
        #    print "cpu is %s and nodename is %s" % (cpu, i.nodename)
        vcpus_total = i.vcpus_total or i.vcpus_used
        if vcpus_total:
<<<<<<< HEAD
            cpu_ratio = colorizer(
                i.vcpus_used * 100.0 / (vcpus_total * i.cpu_allocation_ratio))
=======
            cpu_ratio = colorizer(i.vcpus_used * 100.0 / (vcpus_total * i.cpu_allocation_ratio))
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
        else:
            cpu_ratio = '-'

        ram_used = i.total_usable_ram_mb - i.free_ram_mb
        ram = "%s/%s" % (ram_used, i.total_usable_ram_mb)
        total_usable_ram_mb = i.total_usable_ram_mb or ram_used
        if total_usable_ram_mb:
<<<<<<< HEAD
            ram_ratio = colorizer(
                ram_used * 100.0 /
                (i.total_usable_ram_mb * i.ram_allocation_ratio))
=======
            ram_ratio = colorizer(ram_used * 100.0 / (i.total_usable_ram_mb * i.ram_allocation_ratio))
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
        else:
            ram_ratio = '-'

        disk_used = i.disk_mb_used / 1024.0
        num_instances = 0
        if 'num_instances' in i.stats:
            num_instances = i.stats['num_instances']
        num_vm_active = 0
        if 'num_vm_active' in i.stats:
            num_vm_active = i.stats['num_vm_active']
        num_vm_others = int(num_instances) - int(num_vm_active)
        tbl.add_row([i.host, i.nodename, i.updated, i.host_ip,
                     cpu, cpu_ratio,
                     ram, ram_ratio,
                     num_instances, num_vm_active, num_vm_others])
<<<<<<< HEAD
    print "======================= Hypervisor resource ======================="
=======
    print "============================ Hypervisor resource ============================"
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
    print tbl.get_string(sortby="ip")


def alloction_check():
<<<<<<< HEAD
    print "====================== alloction check ======================"

    tbl = PrettyTable(["status", "hostname", "nodename", "vm_in_nodes",
                       "vm_in_allocations"])
=======
    print "============================ alloction check ============================"

    tbl = PrettyTable(["status", "hostname", "nodename", "vm_in_nodes", "vm_in_allocations"])
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
    tbl.align['hostname'] = 'l'
    tbl.align['nodename'] = 'l'
    hm = host_manager.HostManager()
    states = hm.get_all_host_states(cxt)
    node_vm_map = {}
    for i in states:
        rp = rp_obj.ResourceProvider.get_by_uuid(cxt, i.uuid)
        node_vm_map.setdefault(rp.name, set())
        # import pdb;pdb.set_trace()
        for j in i.instances:
<<<<<<< HEAD
            # Note(fanzhang): j should one Instance object
            # which means instance on node.
=======
            # Note(fanzhang): j should one Instance object which means instance on node.
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
            inst = i.instances[j]
            node_name = inst.node
            node_vm_map.setdefault(node_name, set())
            node_vm_map[node_name].add(inst.uuid)
        # import pdb;pdb.set_trace()
        db_allocs = rp_obj._get_allocations_by_provider_id(cxt, rp.id)
        vms_in_allocation = set()
        for j in db_allocs:
            vms_in_allocation.add(j['consumer_id'])
        vm_in_nodes = node_vm_map[rp.name]
        msg = "%s(%s, %s)\033[0m: vm in nodes: %s <-> vm in allocations: %s"
        if vm_in_nodes == vms_in_allocation:
            hint = "%s%s\033[0m" % (color_tbl['green'], 'OK')
            hostname = "%s%s\033[0m" % (color_tbl['blue'], i.host)
            nodename = "%s%s\033[0m" % (color_tbl['yellow'], i.nodename)
<<<<<<< HEAD
            # print msg % (color_tbl['green'], i.host, i.nodename,
            # len(vm_in_nodes), len(vms_in_allocation))
        else:
            hint = "%s%s\033[0m" % (color_tbl['red'], 'X')
            hostname = "%s%s\033[0m" % (color_tbl['blue'], i.host)
            nodename = "%s%s\033[0m" % (color_tbl['yellow'], i.nodename)
            # print msg % (color_tbl['red'], i.host, i.nodename,
            # len(vm_in_nodes), len(vms_in_allocation))
=======
            # print msg % (color_tbl['green'], i.host, i.nodename, len(vm_in_nodes), len(vms_in_allocation))
        else:
            hint = "%s%s\033[0m" % (color_tbl['red'], 'X')
            hostname = "%s%s\033[0m" % (color_tbl['red'], i.host)
            nodename = "%s%s\033[0m" % (color_tbl['red'], i.nodename)
            # print msg % (color_tbl['red'], i.host, i.nodename, len(vm_in_nodes), len(vms_in_allocation))
>>>>>>> 3e8d07ccfc2b77d50e06ec0dd77a0b6f32cb9ca1
            # print vms_in_allocation - vm_in_nodes
            # print vm_in_nodes - vms_in_allocation
        tbl.add_row([hint, hostname, nodename, len(vm_in_nodes), len(vms_in_allocation)])

    print tbl.get_string(sortby='hostname')


check_services()
print_hypervisor_view()
alloction_check()