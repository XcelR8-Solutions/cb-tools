import json
import requests
from .base import APIBase

class Network(APIBase):

	AWS_ZONE_TYPE = "amazon"
	AZURE_ZONE_TYPE = "azure"
	VCENTER_ZONE_TYPE = "vcenter"

	def __init__(self):
		APIBase.__init__(self)

	def getResourcePools(self, zoneId):
		url = self.apiEndpoint+"/api/zones/"+str(zoneId)+"/resource-pools"
		response = requests.get(url, verify=False, headers=self.headers)
		return json.loads(response.content);

	def createResourcePool(self, zoneId, zoneType, resourcePoolName, cidrBlock):
		url = self.apiEndpoint+"/api/zones/"+str(zoneId)+"/resource-pools"
		payload = {"resourcePool": {
						"name": resourcePoolName,
						"config": {
							"cidrBlock": cidrBlock,
      				 		"tenancy": "default"
    					},
    					"tenantPermissions": {
      						"accounts": [1,2,3,4,5]
    					},
    					"resourcePermissions": {
      						"all": "true",
      						
    					}

    				}
    			}
		#response = requests.post(url, verify=False, headers=self.headers, json=payload)
		#return json.loads(response.content);