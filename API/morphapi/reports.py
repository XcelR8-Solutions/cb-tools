import json
import requests
from .base import APIBase

class Reports(APIBase):

    def __init__(self):
        APIBase.__init__(self)

    def getAccounts(self):
        url = self.apiEndpoint+"/api/accounts"
        response = requests.get(url, verify=False, headers=self.headers)
        return json.loads(response.content);

    def getBilling(self, subAccountId):
        if subAccountId == "all":
            url = self.apiEndpoint+"/api/billing/account"
        else: 
            url = self.apiEndpoint+"/api/billing/account/"+str(subAccountId)
        print(url)
        response = requests.get(url, verify=False, headers=self.headers)
        return json.loads(response.content);
