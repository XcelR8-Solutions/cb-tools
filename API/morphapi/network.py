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
		return json.loads(response.content)

	def getNetworkTypes(self):
		url = self.apiEndpoint+"/api/network-types"
		response = requests.get(url, verify=False, headers=self.headers)
		return json.loads(response.content)

	def getAllSecurityGroupRulesBySG(self, securityGroupId):
		url = self.apiEndpoint+"/api/security-groups/"+str(securityGroupId)+"/rules"

		response = requests.get(url, verify=False, headers=self.headers)

		return json.loads(response.content)

	def getSecurityGroupRule(self, securityGroupId, ruleId):
		url = self.apiEndpoint+"/api/security-groups/"+str(securityGroupId)+"/rules/"+str(ruleId)

		response = requests.get(url, verify=False, headers=self.headeers)

		return json.loads(response.content)

	def createResourcePool(self, zoneId, zoneType, resourcePoolName, cidrBlock):
		url = self.apiEndpoint+"/api/zones/"+str(zoneId)+"/resource-pools"
		
		if zoneType == self.AWS_ZONE_TYPE:
			payload = {
				"resourcePool": {
					"name": resourcePoolName,
					"config": {
						"cidrBlock": cidrBlock,
						"tenancy": "default"
					},
					"resourcePermissions": {
						"all": "true",
						"allPlans": "true"
					}
				}
			}
		
		response = requests.post(url, verify=False, headers=self.headers, json=payload)
		return json.loads(response.content)

	def createNetwork(self, zoneId, networkName, networkDescription, networkTypeId, cidr, resourcePoolId, availabilityZone):
		url = self.apiEndpoint+"/api/networks"

		payload = {
  			"network": {
    			"name": networkName,
    			"description": networkDescription,
    			"zone": {
      				"id": zoneId
    			},
    			"type": {
      				"id": networkTypeId
    			},
    			"cidr": cidr,
    			"zonePool": {
      				"id": resourcePoolId
    			},
    			"dhcpServer": "on",
    			"availabilityZone": availabilityZone,
    			"assignPublicIp": "on",
    			"scanNetwork": "off",
    			"applianceUrlProxyBypass": "on",
    			"noProxy": "null"
  			},
  			"resourcePermissions": {
   				"all": "true"
  			}
		}
		
		response = requests.post(url, verify=False, headers=self.headers, json=payload)
		return json.loads(response.content)

	def createSecurityGroup(self, sgName, sgDesc, zoneId, resourcePoolId):
		url = self.apiEndpoint+"/api/security-groups"

		payload = {
			"securityGroup": {
    			"name": sgName,
    			"description": sgDesc,
    			"zoneId": zoneId,
    			"customOptions": {
    				"vpc" : resourcePoolId
    			}
  			}
		}

		response = requests.post(url, verify=False, headers=self.headers, json=payload)
		return json.loads(response.content)

	def createSecurityGroupRule(self, securityGroupId, name, direction, ruleType, protocol, portRange, sourceType, source, destinationType):
		url = self.apiEndpoint+"/api/security-groups/"+str(securityGroupId)+"/rules"
		
		payload = {
			"rule": {
    			"name": name,
    			"direction": direction,
    			"ruleType": ruleType,
    			"protocol": protocol,
    			"portRange": portRange,
    			"sourceType": sourceType,
    			"source": source,
    			"destinationType": destinationType
  			}
		}
		
		response = requests.post(url, verify=False, headers=self.headers, json=payload)
		return json.loads(response.content)

	def deleteSecurityGroupRule(self, securityGroupId, ruleId):
		url = self.apiEndpoint+"/api/security-groups/"+str(securityGroupId)+"/rules/"+str(ruleId)

		response = requests.delete(url, verify=False, headers=self.headers)

		return json.loads(response.content)

	def deleteSecurityGroup(self, securityGroupId):
		url = self.apiEndpoint+"/api/security-groups/"+str(securityGroupId)

		response = requests.delete(url, verify=False, headers=self.headers)

		return json.loads(response.content)
