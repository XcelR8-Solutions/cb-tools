import json
import requests
from .base import APIBase

class Network(APIBase):

    def __init__(self):
        APIBase.__init__(self)

	def getResourcePools(zoneId):
		url = apiEndpoint+"/api/zones/"+str(zoneId)+"/resource-pools"
		response = requests.get(url, verify=False, headers=headers)
		return json.loads(response.content);