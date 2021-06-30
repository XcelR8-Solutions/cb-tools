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
searchTerm = ""

sys.path.append(appPath)
from morphapi.apps import App

# 1. Build objects and print config
appObj = App()

appObj.printConfig()

###### 
# 1. Get instances
######
appObj.out("Getting apps")
apps = appObj.getApps(searchTerm)
# Print out the apps
for app in apps.get('apps'):
	print("App id["+str(app['id'])+"] name["+app['name']+"] description["+str(app['description'])+"]")
print("\n")
