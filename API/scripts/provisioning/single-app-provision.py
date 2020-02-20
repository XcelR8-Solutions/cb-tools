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
# 3. API, Get app blueprint details
# 4. API, Create app
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
appBpPath = resourcePath + "/*FILE*" #<-- JSON file here

sys.path.append(appPath)
from morphapi.apps import App
from morphapi.cloud import Cloud

# 1. Build objects and print config
appObj = App()
cloudObj = Cloud()

appObj.printConfig()

###### 
# 1. Get app blueprint
###### 
appObj.out("Getting Application Blueprint...")
print(appBpPath)
appBP = appObj.getAppBP(appBpPath)

###### 
# 2. Create App
###### 
appObj.out("Building application...");
appResponse = appObj.runAppCreate(appBP)
print(appResponse);

