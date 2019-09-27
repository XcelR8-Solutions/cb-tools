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

    def modifyAppBPNetwork(self, appBP, bpMods):
        appTier = appBP['tiers']['App']['instances'] if 'App' in appBP['tiers'] else [] 
        cacheTier = appBP['tiers']['Cache']['instances'] if 'Cache' in appBP['tiers'] else [] 
        dbTier = appBP['tiers']['Database']['instances'] if 'Database' in appBP['tiers'] else [] 
        messagingTier = appBP['tiers']['Messaging']['instances'] if 'Messaging' in appBP['tiers'] else [] 
        webTier = appBP['tiers']['Web']['instances'] if 'Web' in appBP['tiers'] else [] 
        instanceList = appTier + cacheTier + dbTier + messagingTier + webTier
        
        for instance in instanceList:
            if bpMods[instance['instance']['name']]:
                 print("*** Modifying Instance ["+instance['instance']['name']+"] ***")
                 instance['config']['resourcePoolId'] = bpMods[instance['instance']['name']]['resourcePoolId']
                 instance['networkInterfaces'][0]['network']['idName'] = bpMods[instance['instance']['name']]['networkName']
                 instance['networkInterfaces'][0]['network']['id'] = bpMods[instance['instance']['name']]['networkId']
                 instance['securityGroups'][0]['id'] = bpMods[instance['instance']['name']]['securityGroup']
        return appBP

    def runAppCreate(self, bluePrint):
        url = self.apiEndpoint+"/api/apps"
        response = requests.post(url, verify=False, headers=self.headers, json=bluePrint)
        return json.loads(response.content);

    def getAppInformation(self, appId):
        url = self.apiEndpoint+"/api/apps/"+str(appId)
        response = requests.get(url, verify=False, headers=self.headers)
        return json.loads(response.content);