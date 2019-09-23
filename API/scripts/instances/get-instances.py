import json
import requests
import urllib
import os

# -------------------
# python3 -m venv morpheus-tools
# source morpheus-tools/bin/activate
# pip install requests
#
# Steps:
# -------------------
# 1. Call API, auth, get bearer token
# 2. Call API, get instances in a cloud
##################################################################

# Define vars
apiEndpoint = os.environ['MORPHEUS_URL']
apiUsername = os.environ['MORPHEUS_USERNAME']
apiPassword = os.environ['MORPHEUS_PASSWORD']

# Disable ssl warnings (for my example)
requests.packages.urllib3.disable_warnings()

# Out()
def out(aString):
	out = "\n--------------------------------------\n"
	out += "| "+ aString+"\n"
	out += "--------------------------------------"
	print(out)

def printConfig():
	out = "\n===============================\n"
	out += "= Config:\n"
	out += "= apiEndpoint="+apiEndpoint+"\n" 
	out += "= apiUsername="+apiUsername+"\n"
	out += "= apiPassword="+apiPassword+"\n"
	out += "===============================\n"
	print(out)

# Auth()
def auth():
	url = apiEndpoint+"/oauth/token?grant_type=password&scope=write&client_id=morph-customer"
	credsJSON = {'username':apiUsername, 'password': apiPassword};
	response = requests.post(url, verify=False, headers='', data=credsJSON)
	authInfo = json.loads(response.content)
	print(authInfo.get('access_token'))
	return authInfo.get('access_token');

# GetInstances()
def getInstances():
	url = apiEndpoint+"/api/instances"
	response = requests.get(url, verify=False, headers=headers)
	return json.loads(response.content).get('instances'); 

printConfig()

# 1. Auth and get bearer token
out("Doing the auth thang...")
apiBearerToken = auth()
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(apiBearerToken)}

# 2. Get instances in a cloud
out("Retrieving Instances...")
instances = getInstances()
for instance in instances:
	print("Instance - ID["+str(instance['id'])+"] Name["+instance['name']+"] Cloud["+instance['cloud']['name']+"]")

