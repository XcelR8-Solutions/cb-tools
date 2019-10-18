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

# Auth()
def auth():
	url = apiEndpoint+"/oauth/token?grant_type=password&scope=write&client_id=morph-customer"
	credsJSON = {'username':apiUsername, 'password': apiPassword};
	response = requests.post(url, verify=False, headers='', data=credsJSON)
	authInfo = json.loads(response.content)
	return authInfo.get('access_token');

# GetInstanceByName()
def getInstanceByName(instanceName):
	matchInstance = ""
	url = apiEndpoint+"/api/instances"
	response = requests.get(url, verify=False, headers=headers)
	iList = json.loads(response.content);
	for instance in iList.get('instances'):
		if instance['name'].strip() == instanceName.strip():
			matchInstance = instance;
			break
	return matchInstance; 

# 1. Auth and get bearer token
apiBearerToken = auth()
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(apiBearerToken)}

# 2. Get instances in a cloud
instance = getInstanceByName('jb-tomcat-1003')
print("IP_ADDR="+instance['connectionInfo'][0]['ip'])

##################################################################
#
# DOCS: https://docs.morpheusdata.com/en/4.0.0/provisioning/automation/automation.html#task-results
#
# To access the above variable in a script (same workflow phase, after this script)
# 1. Set the return type for this task to "Key/Value Pairs"
# 2. In next script output something to this affect:  echo "keyval value: <%=results.keyval.IP_ADDR%>"
#
##################################################################


