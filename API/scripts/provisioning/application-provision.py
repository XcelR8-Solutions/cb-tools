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
cloudCode = "mtaws"
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
cloudObj.out("Getting cloud info for ["+cloudCode+"]")
zone = cloudObj.getZone(cloudCode)

# 3. Build the resource pool
networkObj.out("Building resource pool for zoneId["+str(zone['id'])+"] type["+zone['zoneType']['code']+"]")
resourcePool = networkObj.createResourcePool(zone['id'], zone['zoneType']['code'], "Poopie Pool", "10.1.1.1/28")


#  
# out("Building application...");
# appBP = appObj.getAppBP(appBpPath)
# response = appObj.runAppCreate(appBP)


