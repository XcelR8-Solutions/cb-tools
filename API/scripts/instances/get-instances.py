##################################################################
# 
# File: 
# get-instances.py
#
# Desc: 
# -------------------
# Example for retrieving instance information
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
# 2. API, Get instance list
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

sys.path.append(appPath)
from morphapi.instance import Instance

# 1. Build objects and print config
instanceObj = Instance()

instanceObj.printConfig()

###### 
# 1. Get instances
######
instanceObj.out("Getting instances")
instances = instanceObj.getInstances()
print(instances)
