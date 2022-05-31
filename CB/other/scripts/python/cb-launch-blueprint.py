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
# 2. Build JSON blueprint
# 3. Fire - call API endpoint to create order
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
	return authInfo.get('token')

# GetInstances()
def runBlueprint(jsonBlueprint):
	url = apiEndpoint+"/api/v2/orders/"
	response = requests.post(url, verify=False, headers=headers, data=jsonBlueprint)
	return json.loads(response.content) 

printConfig()

# 1. Auth and get bearer token
out("Doing the auth thang...")
apiBearerToken = auth()
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(apiBearerToken)}

# 2. Get instances in a cloud
out("Running Blueprint...")
jsonBlueprint = """
{
    "group": "/api/v2/groups/GRP-4ocssk7c/",
    "items": {
        "deploy-items": [
            {
                "blueprint": "/api/v2/blueprints/BP-df7476du/",
                "blueprint-items-arguments": {
                    "build-item-Ubuntu-18.04-Build": {
                        "attributes": {
							"hostname": "jeffb-from-api-yo",
                            "quantity": 1
                        },
                        "environment": "/api/v2/environments/ENV-ul7zw3s2/",
                        "os-build": "/api/v2/os-builds/OSB-2qeptzs2/",
                        "parameters": {
                            "enable-monitoring": "False"
                        }
                    }
                },
                "resource-name": "ubuntu1804",
                "resource-parameters": {}
            }
        ]
    },
    "submit-now": "true"
}"""

runResponse = runBlueprint(jsonBlueprint)
print(runResponse)

