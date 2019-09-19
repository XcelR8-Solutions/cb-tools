import json
import requests
from .base import APIBase

class App(APIBase):

    def __init__(self):
        APIBase.__init__(self)

    def getAppBP(self, fileToOpen):
        # read in from a file
        with open(fileToOpen, 'r') as f:
            bp = json.load(f)
        return bp

    def runAppCreate(self, bluePrint):
        url = self.apiEndpoint+"/api/apps"
        response = requests.post(url, verify=False, headers=self.headers, json=bluePrint)
        return json.loads(response.content);

    def getAppInformation(self, appId):
        url = self.apiEndpoint+"/api/apps/"+str(appId)
        response = requests.get(url, verify=False, headers=self.headers)
        return json.loads(response.content);