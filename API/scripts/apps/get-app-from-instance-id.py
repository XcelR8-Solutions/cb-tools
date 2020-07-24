##################################################################
# 
# File: 
# get-apps.py
#
# Desc: 
# -------------------
# Example for retrieving running apps in Morpheus
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
# 2. API, Get apps list
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
instanceId = "9"

sys.path.append(appPath)
from morphapi.apps import App
from morphapi.instance import Instance

# 1. Build objects and print config
appObj = App()
instanceObj = Instance()

instanceObj.printConfig()

###### 
# 1. Get instances
######
instanceObj.out("Getting instance for id["+instanceId+"]...")
instance = instanceObj.getIntanceById(instanceId)
# Print out the instance info
print(instance)
print("\n")
