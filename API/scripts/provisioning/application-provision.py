import json
import requests
import urllib
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../..'))
from morphapi.apps import App

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

appObj = App()
appObj.printConfig()

networkBP = {}

# 2. Run Terraform create
#out("Running the network create in TF...");
#networkAppInfo = runAppCreate(getAppBP())
#print(networkAppInfo)

# 3. Get resource pools for the desired cloud
#out("Getting resource pools...");
#zone = getZone("mtaws");
#resourcePools = getResourcePools(zone.get('id'))
#print(resourcePools)

