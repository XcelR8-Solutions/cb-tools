import json
import requests
from .base import APIBase

class Instance(APIBase):
	
	def __init__(self):
		APIBase.__init__(self)

	def getInstances(self):
		url = self.apiEndpoint+"/api/instances"
		response = requests.get(url, verify=False, headers=self.headers)
		return json.loads(response.content);

	def getInstanceByName(self, instanceName):
		matchInstance = ""
		url = self.apiEndpoint+"/api/instances"
		response = requests.get(url, verify=False, headers=self.headers)
		iList = json.loads(response.content);
		for instance in iList.get('instances'):
			if instance['name'].strip() == instanceName.strip():
				matchInstance = instance;
				break
		return matchInstance; 

	def getIntanceById(self, instanceId):
		url = self.apiEndpoint+"/api/instances"
		response = requests.get(url, verify=False, headers=self.headers)
		return json.loads(response.content);