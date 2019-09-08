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
# 3. Call API, get tasks
# 4. Call API, exec task against group of instances
##################################################################

# Define vars
apiEndpoint = os.environ['TECHM_MORPHEUS_URL']
apiUsername = os.environ['TECHM_MORPHEUS_USERNAME']
apiPassword = os.environ['TECHM_MORPHEUS_PASSWORD']

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

# GetTasks()
def getTaskByCode(taskCode):
	theTask = ""
	url = apiEndpoint+"/api/tasks"
	response = requests.get(url, verify=False, headers=headers)
	tasks = json.loads(response.content)
	for task in tasks.get('tasks'):
		if task['code'] == taskCode:
			theTask = task
			break
	return theTask;

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

# 3. Get tasks
out("Retrieving Task by Code[linuxApplyPatches]..")
task = getTaskByCode('linuxApplyPatches')
print("Task ID["+str(task['id'])+"] Code["+task['code']+"] Name["+task['name']+"]")

# 4. Exec task on instances
out("Running patch job on instances..")
script = task['taskOptions']['script']
for instance in instances:
	print("PATCHING :: Instance ["+instance['name']+"] with script["+task['name']+"]")
	# call API here
	url = apiEndpoint+"/api/execution-request/execute?instanceId="+str(instance['id'])
	payload = {'script': script}
	response = requests.post(url, verify=False, headers=headers, json=payload)

