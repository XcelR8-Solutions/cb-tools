##################################################################
# 
# File: 
# application-provision.py
#
# Desc: 
# -------------------
# Example for application provisioning via the Morpheus API
#
# Requirements:
# -------------------
# python3 -m venv morpheus-tools
# source morpheus-tools/bin/activate
# pip install requests
#
#
# Steps:
# -------------------
# 1. API, Auth
# 2. API, Get cloud details
# 3. API, Build new resource pool
# 4. API, BUild 2x networks on resource pool from #3
# 5. API, Build new security groups on resource pool from #3
# 6. API, Get cloud info (vpc, subnet, security group)
# 7. API, Get app blueprint details
# 8. Substitute in network bits into app blueprint IaC
# 9. API, Create app
#
##################################################################

import json
import requests
import urllib
import sys
import os

# Set vars
# TODO Move this into a config file
appPath = os.path.abspath(os.path.dirname(__file__) + '../..')
resourcePath = appPath + "/resources"
networkBpPath = resourcePath + "/AWSNetwork-config.json"
appBpPath = resourcePath + "/2Tier-App-config.json"
awsCloudCode = "mtaws"
awsVPCname = "vpc-script-gen"
awsVPCcidr = "172.32.0.0/16"
awsSubnet1cidr = "172.32.0.0/20"
awsSubnet2cidr = "172.32.16.0/20"
awsAVzone1 = "us-west-1b"
awsAVzone2 = "us-west-1c"

sys.path.append(appPath)
from morphapi.apps import App
from morphapi.cloud import Cloud
from morphapi.network import Network

# 1. Build objects and print config
appObj = App()
cloudObj = Cloud()
networkObj = Network()

appObj.printConfig()

# 2. Get cloud details
cloudObj.out("Getting cloud info for ["+awsCloudCode+"]")
zone = cloudObj.getZone(awsCloudCode)

# 3. Build the resource pool
networkObj.out("Building resource pool for zoneId["+str(zone['id'])+"] type["+zone['zoneType']['code']+"]")
response = networkObj.createResourcePool(zone['id'], zone['zoneType']['code'], awsVPCname, awsVPCcidr)
print("Created ResourcePool id["+str(response['resourcePool']['id'])+"] name["+response['resourcePool']['name']+"]")

# 4. Build the networks
networkObj.out("Building networks for rpId["+str(response['resourcePool']['id'])+"] rpName["+response['resourcePool']['name']+"]")
subnet1 = networkObj.createNetwork(zone['id'], awsSubnet1cidr+" - (aws subnet)", "aws network #1", 34, awsSubnet1cidr, response['resourcePool']['id'], awsAVzone1)
subnet2 = networkObj.createNetwork(zone['id'], awsSubnet2cidr+" - (aws subnet)", "aws network #2", 34, awsSubnet2cidr, response['resourcePool']['id'], awsAVzone2)
print("Created subnet1 on ResourcePool ["+response['resourcePool']['name']+"] subnet["+subnet1['network']['name']+"]")
print("Created subnet2 on ResourcePool ["+response['resourcePool']['name']+"] subnet["+subnet2['network']['name']+"]")
# TODO : maybe make this dynamic 
#networkTypes = networkObj.getNetworkTypes()

#  
# out("Building application...");
# appBP = appObj.getAppBP(appBpPath)
# response = appObj.runAppCreate(appBP)


