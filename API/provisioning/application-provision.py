import json
import requests
import urllib

##################################################################
# bfc7c347-1689-40be-b271-657e17afd957
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
# Steps:
# -------------------
# 1. Set up terraform blueprint for network
# 2. Set up app blueprint for app (Morpheus DSL)
# 3. Call API, auth, get bearer token
# 4. Call API, create tf app
# 5. Take return payload and store in object
# 6. Manipulate app payload with details from tf return
# 7. Call API, create app
# 8. Capture return
##################################################################

# Define vars


# Disable ssl warnings (for my example)
requests.packages.urllib3.disable_warnings()

# Out()
def out(aString):
	out = "\n--------------------------------------\n"
	out += "| "+ aString+"\n"
	out += "--------------------------------------"
	print(out)

# Auth()
def auth():
	url = apiEndpoint+"/oauth/token?grant_type=password&scope=write&client_id=morph-customer"
	credsJSON = {'username':apiUsername, 'password': apiPassword};
	response = requests.post(url, verify=False, headers='', data=credsJSON)
	authInfo = json.loads(response.content)
	print(authInfo.get('access_token'))
	return authInfo.get('access_token');

def getNetworkBP():
	return {
  			"id": 2,
  			"image": "https://10.30.20.180/storage/logos/uploads/AppTemplate/2/templateImage/network_original.png",
  			"name": "AWSNetwork",
  			"description": "AWSNetwork",
  			
  			"type": "terraform",
  			"category": "network",
  			"templateName": "AWSNetwork",
  			"defaultCluster": 'null',
  			"defaultPool": 'null',
  			"needsReset": 'true',
  			"group": {
    			"id": 1,
    			"name": "jb-public-group"
  			},
  			"environment": "Dev",
  			"envCode": "dev"
		}

def runAppCreate(bp):
	url = apiEndpoint+"/api/apps"
	response = requests.post(url, verify=False, headers=headers, json=bp)
	return json.loads(response.content);

def getAppInformation(appId):
	url = apiEndpoint+"/api/apps/"+str(appId)
	response = requests.get(url, verify=False, headers=headers)
	return json.loads(response.content);

def getZone(zoneCode):
	cloud = ""
	url = apiEndpoint+"/api/zones"
	response = requests.get(url, verify=False, headers=headers)
	zList = json.loads(response.content);
	for zone in zList.get('zones'):
		if zone.get("code") == zoneCode:
			cloud = zone;
			break
	return cloud

def getResourcePools(zoneId):
	url = apiEndpoint+"/api/zones/"+str(zoneId)+"/resource-pools"
	response = requests.get(url, verify=False, headers=headers)
	return json.loads(response.content);


# 1. Auth and get bearer token
out("Doing the auth thang...")
apiBearerToken = auth()
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(apiBearerToken)}

# 2. Run Terraform create
out("Running the network create in TF...");
networkAppInfo = runAppCreate(getNetworkBP())
print(networkAppInfo)

# 3. Get resource pools for the desired cloud
out("Getting resource pools...");
zone = getZone("mtaws");
resourcePools = getResourcePools(zone.get('id'))
print(resourcePools)

