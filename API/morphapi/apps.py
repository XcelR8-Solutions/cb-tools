import json
import requests
from .base import APIBase

class App(APIBase):

    def __init__(self):
        APIBase.__init__(self)

    def getAppBP(self):
        bp = {}
        print("headers="+str(self.headers));
        return bp

    def runAppCreate(self):
        url = apiEndpoint+"/api/apps"
        response = requests.post(url, verify=False, headers=self.headers, json=bp)
        return json.loads(response.content);

    def getAppInformation(self, appId):
        url = apiEndpoint+"/api/apps/"+str(appId)
        response = requests.get(url, verify=False, headers=self.headers)
        return json.loads(response.content);