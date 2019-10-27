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
# 2. Call API, create postgres check
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

# createPostgresDbCheck
def createPostgresDbCheck(checkName, dbHost, dbPort, dbUser, dbPassword, dbName, dbQuery, checkOperator, checkResult):
	url = apiEndpoint+"/api/monitoring/checks"
	payload = {
  		"check": {
	    	"name": checkName,
	    	"checkType": {
	    		"code": "postgresCheck"
	    	},
	    	"inUptime": "true",
	    	"severity": "critical",
	    	"description": "null",
	    	"checkInterval": 300,
	    	"checkAgent": "null",
	    	"active": "true",
	    	"config": {
	    		"dbHost":dbHost,
	    		"dbPort": dbPort, 
	    		"dbUser":dbUser,
	    		"dbPassword":dbPassword, 
	    		"dbName": dbName, 
	    		"dbQuery": dbQuery, 
	    		"checkOperator": checkOperator, 
	    		"checkResult": checkResult
	    	}
		}
	}
	response = requests.post(url, verify=False, headers=headers, json=payload)
	return json.loads(response.content); 

# 1. Auth and get bearer token
apiBearerToken = auth()
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(apiBearerToken)}

# 2. Create 
postgresDbCheck = createPostgresDbCheck('Sample Postgres Check', '10.30.20.151', '10000', 'jjbrassa', 'd00kie!!', 'jjbrassa', 'select * from tester', 'lt', '2')
print(postgresDbCheck)



