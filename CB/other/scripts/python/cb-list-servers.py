import json
import requests
import urllib
import os

# -------------------
# pip install requests
#
# Steps:
# -------------------
# 1. Call API, auth, get bearer token
# 2. 
##################################################################

# Define vars
apiEndpoint = os.environ['CB_URL']
apiUsername = os.environ['CB_USERNAME']
apiPassword = os.environ['CB_PASSWORD']

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
	url = apiEndpoint+"/api/v2/api-token-auth/"
	credsJSON = {'username':apiUsername, 'password': apiPassword};
	response = requests.post(url, verify=False, headers='', data=credsJSON)
	authInfo = json.loads(response.content)
	print(authInfo.get('token'))
	return authInfo.get('token');

# GetInstances()
def getServers():
	url = apiEndpoint+"/api/v2/servers/"
	response = requests.get(url, verify=False, headers=headers)
	return json.loads(response.content).get('_embedded'); 

printConfig()

# 1. Auth and get bearer token
out("Doing the auth thang...")
apiBearerToken = auth()
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(apiBearerToken)}

# 2. Get instances in a cloud
out("Retrieving Servers...")
servers = getServers()
for server in servers:
	print("Server ["+server['hostname']+"]")

