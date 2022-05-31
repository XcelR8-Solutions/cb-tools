"""
RUN : As a pre-create task on a provision server orchestration
TARGET: Azure

Will do the following:
----------------------
1. Re-sync the environment networks and RGs
2. Associate the new RG with the server before provision
3. Associate the new vnet/subnet with the server before provision

"""
import time
from common.methods import set_progress
from resourcehandlers.models import ResourceNetwork


def run(job, *args, **kwargs):
    resource_group = ""
    network_name = ""

    # 1. Grab params
    params = job.job_parameters.cast()
    bp_job_params = job.parent_job.job_parameters.cast()

    # 2. Refresh RGs and Networks
    order = job.get_order()
    server = job.server_set.first()
    env = server.environment
    rh = server.resource_handler.cast()
    set_progress("Refreshing Environment[" + env.name + "] with new RG and VNet/Subnet")
    rh.import_parameters_for_env(env, 'resource_group_arm')
    rh.sync_subnets(env)

    # 3. Set new goodies and save!
    bp_params = bp_job_params.blueprintitemarguments_set.first()
    lz_values = bp_params.get_cf_values_as_dict()
    for key, value in lz_values.items():
        if key.find("virtual_net_name") >= 0:
            network_name = vnet_name = value + '/' + value + '_subnet'
        elif key.find("resource_group") >= 0:
            resource_group = value

    set_progress(
        "Updating server[" + server.get_vm_name() + "] rg[" + resource_group + "] subnet[" + network_name + "]")
    new_rn = ResourceNetwork.objects.get(name=network_name)
    server.sc_nic_0 = new_rn
    server.resource_group_arm = resource_group
    server.save()

    if True:
        return "SUCCESS", "Successfully associated workload with RG/VNet/Subnet", ""
    else:
        return "FAILURE", "Unable to associate workload with RG/VNet/Subnet", "Unable to associate workload with RG/VNet/Subnet"