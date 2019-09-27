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
# 6. API, Build rules on new security group from #5
# 7. API, Get app blueprint details
# 8. Substitute in network bits into app blueprint IaC
# 9. API, Create app
# 10. API, Call TF app create for additional network setup
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
awsVPCname = "vpc-for-application"
awsVPCCIDR = "172.32.0.0/16"
awsAppSubnetCIDR = "172.32.0.0/20"
awsDBSubnetCIDR = "172.32.16.0/20"
awsAVzone1 = "us-west-1b"
awsAVzone2 = "us-west-1c"
awsSecurityGroupName = "aws-application-sg"
awsSecurityGroupDesc = "Application Security Group"

sys.path.append(appPath)
from morphapi.apps import App
from morphapi.cloud import Cloud
from morphapi.network import Network

# 1. Build objects and print config
appObj = App()
cloudObj = Cloud()
networkObj = Network()

appObj.printConfig()

# TODO : Put script run variable to build for cloud target
# code here (parameters off command line)

###### 
# 2. Get cloud details
######
cloudObj.out("Getting cloud info for ["+awsCloudCode+"]")
zone = cloudObj.getZone(awsCloudCode)

###### 
# 3. Build the resource pool
###### 
networkObj.out("Building resource pool for zoneId["+str(zone['id'])+"] type["+zone['zoneType']['code']+"]")
response = networkObj.createResourcePool(zone['id'], zone['zoneType']['code'], awsVPCname, awsVPCCIDR)
resourcePool = response['resourcePool']
print("Created ResourcePool externalId["+resourcePool['externalId']+"] name["+resourcePool['name']+"]")

###### 
# 4. Build the networks
###### 
networkObj.out("Building networks for rpId["+str(response['resourcePool']['id'])+"] rpName["+response['resourcePool']['name']+"]")
appSubnet = networkObj.createNetwork(zone['id'], awsAppSubnetCIDR+" - (app)", "aws app network", 34, awsAppSubnetCIDR, resourcePool['id'], awsAVzone1)
dbSubnet = networkObj.createNetwork(zone['id'], awsDBSubnetCIDR+" - (db)", "aws db network", 34, awsDBSubnetCIDR, resourcePool['id'], awsAVzone2)
print("Created appSubnet on ResourcePool ["+resourcePool['name']+"] subnet["+appSubnet['network']['name']+"]")
print("Created dbSubnet on ResourcePool ["+resourcePool['name']+"] subnet["+dbSubnet['network']['name']+"]")
# TODO : maybe make this dynamic? 
#networkTypes = networkObj.getNetworkTypes()

###### 
# 5. Build security groups
###### 
networkObj.out("Building security group for zoneId["+str(zone['id'])+"] securityGroup["+awsSecurityGroupName+"]")
sg1 = networkObj.createSecurityGroup(awsSecurityGroupName, awsSecurityGroupDesc, zone['id'], resourcePool['externalId'])
securityGroup = sg1['securityGroup']
print("Created security group name["+securityGroup['name']+"] in cloud["+zone['name']+"] for resourcePool["+resourcePool['externalId']+"]")

###### 
# 6. Build security group rules
###### 
networkObj.out("Building security group rules for id["+str(securityGroup['id'])+"] securityGroup["+awsSecurityGroupName+"]")
sgrResponse1 = networkObj.createSecurityGroupRule(securityGroup['id'], "80-in", "ingress", "customRule", "tcp", "80", "network", "0.0.0.0/0", "instance")
sgrResponse2 = networkObj.createSecurityGroupRule(securityGroup['id'], "443-in", "ingress", "customRule", "tcp", "443", "network", "0.0.0.0/0", "instance")
rule1 = sgrResponse1['rule']
rule2 = sgrResponse2['rule']
print("Finished creating security group rule #1 - id["+str(rule1['id'])+"] name["+rule1['name']+"]")
print("Finished creating security group rule #2 - id["+str(rule2['id'])+"] name["+rule2['name']+"]")

###### 
# 7. Get app blueprint
###### 
appObj.out("Getting Application Blueprint...")
print(appBpPath)
appBP = appObj.getAppBP(appBpPath)

###### 
# 8. Merge network info into blueprint
###### 
appObj.out("Modifying Application Blueprint...")
bpMods = {
	"tomcat-node-1": {
		"resourcePoolId": resourcePool['id'],
		"networkId": "network-"+str(appSubnet['network']['id']),
		"networkName": appSubnet['network']['name'],
		"securityGroup": securityGroup['externalId']
	"mysql-node-1": {
		"resourcePoolId": resourcePool['id'],
		"networkId": "network-"+str(dbSubnet['network']['id']),
		"networkName": dbSubnet['network']['name'],
		"securityGroup": securityGroup['externalId']
	}
}
modifiedAppBP = appObj.modifyAppBPNetwork(appBP, bpMods)

###### 
# 9. Create App
###### 
appObj.out("Building application...");
appResponse = appObj.runAppCreate(appBP)
print(appResponse);

###### 
# 10. Create TF App
###### 
# TODO

