"""
Delete an Azure virtual network.
"""
from common.methods import set_progress
from azure.common.credentials import ServicePrincipalCredentials
from msrestazure.azure_exceptions import CloudError
from resourcehandlers.azure_arm.models import AzureARMHandler
from azure.mgmt.network import NetworkManagementClient

###
# Main run() method
###
def run(job, **kwargs):

    # 1. Get attributes stored on meta data
    resource = kwargs.pop('resources').first()
    virtual_net_name = resource.attributes.get(field__name='azure_virtual_net_name').value
    resource_group = resource.attributes.get(field__name='resource_group_name').value
    rh_id = resource.attributes.get(field__name='azure_rh_id').value
    rh = AzureARMHandler.objects.get(id=rh_id)

    # 2. Connect to Azure
    set_progress("Connecting To Azure...")
    credentials = ServicePrincipalCredentials(
        client_id=rh.client_id,
        secret=rh.secret,
        tenant=rh.azure_tenant_id,
    )
    network_client = NetworkManagementClient(credentials, rh.serviceaccount)
    set_progress("Connection to Azure established")

    # 3. Delete VNet
    set_progress("Deleting virtual network %s..." % (virtual_net_name))
    try:
        network_client.virtual_networks.delete(resource_group_name=resource_group, virtual_network_name=virtual_net_name)
    except CloudError as e:
        set_progress("Azure Clouderror: {}".format(e))
        return "FAILURE", "Virtual network could not be deleted", ""

    # 4. Return results
    return "SUCCESS", "The virtual net has been succesfully deleted", ""
