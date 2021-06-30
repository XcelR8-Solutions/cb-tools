import json
import requests
from .base import APIBase

class Monitoring(APIBase):

    def __init__(self):
        APIBase.__init__(self)

    def createPostgresDbCheck(self, checkName, dbHost, dbPort, dbUser, dbPassword, dbName, dbQuery, checkOperator, checkResult):
        url = self.apiEndpoint+"/api/monitoring/checks"
        payload = {
            "check": {
                "name": checkName,
                "checkType": {
                    "code": "postgresCheck"
                },
                "inUptime": "true",
                "severity": "critical",
                "description": "null",
                "checkInterval": 300,
                "checkAgent": "null",
                "active": "true",
                "config": {
                    "dbHost":dbHost,
                    "dbPort": dbPort, 
                    "dbUser":dbUser,
                    "dbPassword":dbPassword, 
                    "dbName": dbName, 
                    "dbQuery": dbQuery, 
                    "checkOperator": checkOperator, 
                    "checkResult": checkResult
                }
            }
        }
        response = requests.post(url, verify=False, headers=self.headers, json=payload)
        return json.loads(response.content); 

    def createWebGetCheck(checkName, webGetCheckUrl):
        url = apiEndpoint+"/api/monitoring/checks"
        payload = {
            "check": {
                "name": checkName,
                "checkType": {
                    "code": "webGetCheck"
                },
                "inUptime": "true",
                "severity": "critical",
                "description": "null",
                "checkInterval": 300,
                "checkAgent": "null",
                "active": "true",
                "config": {
                    "webMethod": "GET",
                    "webUrl": webGetCheckUrl
                }
            }
        }
        response = requests.post(url, verify=False, headers=headers, json=payload)
        return json.loads(response.content); 