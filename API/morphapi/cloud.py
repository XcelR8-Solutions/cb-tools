import json
import requests
from .base import APIBase

class Cloud(APIBase):
	
	def __init__(self):
		APIBase.__init__(self)

	def getZone(self, zoneCode):
		url = self.apiEndpoint+"/api/zones"
		response = requests.get(url, verify=False, headers=self.headers)
		zList = json.loads(response.content);
		for zone in zList.get('zones'):
			if zone.get("code") == zoneCode:
				cloud = zone;
				break
		return  cloud