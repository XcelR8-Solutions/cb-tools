import requests
import json
import os

# Disable ssl warnings (for my example)
requests.packages.urllib3.disable_warnings()

class APIBase(object):

    def __init__(self):
        self.apiEndpoint = os.environ['MORPHEUS_URL']
        self.apiUsername = os.environ['MORPHEUS_USERNAME']
        self.apiPassword = os.environ['MORPHEUS_PASSWORD']
        
        url = self.apiEndpoint+"/oauth/token?grant_type=password&scope=write&client_id=morph-customer"
        credsJSON = {'username': self.apiUsername, 'password': self.apiPassword};
        response = requests.post(url, verify=False, headers='', data=credsJSON)
        authInfo = json.loads(response.content)

        self.bearerToken = authInfo['access_token']
        self.headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(self.bearerToken)}

    def out(self, aString):
        out = "\n----------------------------------------------------------\n"
        out += "| "+ aString+"\n"
        out += "----------------------------------------------------------"
        print(out)

    def printConfig(self):
        out = "\n==================================================\n"
        out += "= Config:\n"
        out += "= apiEndpoint="+self.apiEndpoint+"\n" 
        out += "= apiUsername="+self.apiUsername+"\n"
        out += "= apiPassword="+self.apiPassword+"\n"
        out += "= Token="+self.bearerToken+"\n"
        out += "==================================================\n"
        print(out)