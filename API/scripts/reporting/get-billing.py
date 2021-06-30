##################################################################
# 
# File: 
# get-billing.py
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
# 2. API, Get accounts (tenants)
# 3. API, Get billing 
#
##################################################################

import json
import requests
import urllib
import sys
import os

# Disable ssl warnings (for my example)
requests.packages.urllib3.disable_warnings()

# Set vars
appPath = os.path.abspath(os.path.dirname(__file__) + '../..')
sys.path.append(appPath)

from morphapi.reports import Reports

# 1. Build objects and print config
reportsObj = Reports()

reportsObj.printConfig()

# 2. Get accounts
reportsObj.out("Retrieving all accounts (tenants)");
accounts = reportsObj.getAccounts();
for account in accounts['accounts']:
	print("Account id["+str(account['id'])+"] name["+account['name']+"]");

# 3. Get billing
reportsObj.out("Retrieving billing details");
billingDeets = reportsObj.getBilling(2);
print("Billing Deets - name["+billingDeets['billingInfo']['name']+"] startDate["+billingDeets['billingInfo']['startDate']+"] endDate["+billingDeets['billingInfo']['endDate']+"] price["+str(billingDeets['billingInfo']['price'])+"]");
