# CloudBolt Azure LZ (Landing Zone) Blueprint

## Function
This blueprint automates the process of setting up a new Azure Resource Group, VNet, and Subnet.

####Blueprint flow:
1. User is asked to choose from available list of Azure RHs
2. User specifies the Resource Group name
3. User specifies the VNet Name
4. User specifies the VNet Address Space
5. User specifies the Subnet Address space

## Configuration
1. Copy all files in this directory to your CloudBolt appliance. The files can live wherever you would like under */var/opt/cloudbolt/proserv*, but we recommend placing them under */var/opt/cloudbolt/proserv/azure_lz*
2. Map the following file to the blueprint BUILD Tab:  *azure-create-lz.py*
3. Map the following file to the blueprint DISCOVERY Tab:  *azure-sync-vnet.py*
4. Map the following file to the blueprint TEARDOWN Tab:  *azure-delete-lz.py*
