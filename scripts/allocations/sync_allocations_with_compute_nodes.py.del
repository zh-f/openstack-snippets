import sys

from oslo_log import log as logging
from nova import config
from nova import objects
from nova import context
from nova import compute
from nova.objects import resource_provider as rp_obj
from nova.scheduler import client as scheduler_client
from nova.scheduler import host_manager
import nova.conf

CONF = nova.conf.CONF
LOG = logging.getLogger('allocation')


def log_redo_sql(allocations, allocation_id):
    db_allocations = filter(lambda x: x.id == allocation_id, allocations)
    for db_allocation in db_allocations:
        LOG.info('To redo, you can run SQL :::::::::::::::::::')
        LOG.debug(db_allocation.__dict__)
        table_name = db_allocation.__tablename__
        created_at = db_allocation.created_at
        updated_at = db_allocation.updated_at or 'NULL'
        id = db_allocation.id
        resource_provider_id = db_allocation.resource_provider_id
        resource_class_id = db_allocation.resource_class_id
        used = db_allocation.used
        consumer_id = db_allocation.consumer_id or 'NULL'
        sql = ("insert into %s ("
               "created_at, updated_at, id, resource_provider_id, "
               "consumer_id, resource_class_id, used"
               ") values ('%s', %s, %s, %s, '%s', %s, %s);" %
               (table_name, created_at, updated_at, id, resource_provider_id,
                consumer_id, resource_class_id, used))
        LOG.info(sql)


def allocation_sync(cxt):
    hm = host_manager.HostManager()
    states = hm.get_all_host_states(cxt)
    compute_api = compute.API()
    node_vm_map = {}
    for state in states:
        rp_uuid = state.uuid
        rp = rp_obj.ResourceProvider.get_by_uuid(cxt, rp_uuid)

        # NOTE(fanzhang): Constructing a mapping of instance lists on node
        # and node name
        node_vm_map.setdefault(rp.name, set())
        for instance_uuid in state.instances:
            instance_obj = state.instances[instance_uuid]
            node_name = instance_obj.node
            node_vm_map.setdefault(node_name, set())
            node_vm_map[node_name].add(instance_uuid)
            LOG.debug("Instance uuid is %s", instance_uuid)
        vms_in_node = node_vm_map[rp.name]

        allocations_list = rp_obj.AllocationList.\
            get_all_by_resource_provider(cxt, rp)
        LOG.debug('AllocationList is %s', allocations_list)
        vms_in_allocation = set(map(lambda x: x.consumer_id, allocations_list))

        if vms_in_node != vms_in_allocation:
            LOG.warn('Instances on node %s do not match allocations %s',
                     vms_in_node, vms_in_allocation)

        # NOTE(fanzhang): Delete allocations of vms which not on compute nodes
        allocations_more = vms_in_allocation - vms_in_node
        if allocations_more:
            LOG.warn('Instances in allocations are more than those on node: %s'
                     , allocations_more)
            for allocation in allocations_list:
                if allocation.consumer_id in allocations_more:
                    allocs = rp_obj.AllocationList.get_all_by_consumer_id(
                            cxt, consumer_id=allocation.consumer_id)
                    LOG.info('Try to delete %s', allocation)
                    LOG.debug('Allocations by consumer id are %s', allocs)
                    log_redo_sql(allocs, allocation.id)
                    allocation.destroy()

        # NOTE(fanzhang): Create allocations for vms on compute nodes without
        # allocation records.
        host_manager_more = vms_in_node - vms_in_allocation
        if host_manager_more:
            LOG.warn('Instances on nodes are more than allocations: %s'
                     , host_manager_more)
            for instance_uuid in host_manager_more:
                instance = compute_api.get(cxt, instance_uuid)
                LOG.debug(instance)
                LOG.info('Create allocation record with '
                         'resource provider uuid is %s and consumer id is: %s',
                         rp_uuid, instance.uuid)
                scheduler_client.SchedulerClient().reportclien.\
                    _allocate_for_instance(rp_uuid, instance)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        config.parse_args(sys.argv)
    else:
        config.parse_args([sys.argv[0],
                           '--config-file',
                           '/etc/nova/nova.conf'])
    CONF.debug = False
    logging.setup(CONF, 'foo')
    objects.register_all()

    cxt = context.get_admin_context()
    allocation_sync(cxt)