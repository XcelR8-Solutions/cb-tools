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
# 2. Call API, get IP of machine
# 3. Call API, create socket check
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

# createSocketCheck
def createSocketCheck(checkName, host, port, sendBits, responseMatch):
	url = apiEndpoint+"/api/monitoring/checks"
	payload = {
		"check": {
      "name": checkName,
    	"checkType": {
        "code": "socketCheck"
      },
    	"inUptime": "true",
    	"severity": "critical",
    	"description": "null",
    	"checkInterval": 300,
    	"checkAgent": "null",
    	"active": "true",
    	"config": {
        "host": host,
        "port": port, 
        "send": sendBits,
        "responseMatch": responseMatch
      }
  	}
  }
	response = requests.post(url, verify=False, headers=headers, json=payload)
	return json.loads(response.content); 

# 1. Auth and get bearer token
apiBearerToken = auth()
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(apiBearerToken)}

# 2. Get IP of machine to build check for
instanceDetails = getInstanceByName('jb-apache-server')
instanceIP = instanceDetails['connectionInfo'][0]['ip']
print('Creating Socket Check monitor for ['+instanceIP+'] on port[22]')

# 3. Create web check 
socketCheck = createSocketCheck('Sample Socket Check', instanceIP, 22, 'test', 'OK')
print(socketCheck)


