#!/bin/sh
#
# Builds a web monitor
#

MORPHEUS_URL="https://10.30.20.17"

##
# Authenticate
## 
AUTH_TOKEN=$(curl -k -X POST --data "username=$MORPHEUS_USERNAME&password=$MORPHEUS_PASSWORD" "$MORPHEUS_URL/oauth/token?grant_type=password&scope=write&client_id=morph-customer")
ACCESS_TOKEN=$(sed -E 's/.*"access_token":"?([^,"]*)"?.*/\1/' <<< $AUTH_TOKEN)

##
# Grab vars
##
INTERNAL_IP="<%=server.internalIp%>"
EXTERNAL_IP="<%=server.externalIp%>"
SERVER_NAME="<%=server.name%>"

##
# Echo Bits
##
echo "internalip=$INTERNAL_IP"
echo "externalip=$EXTERNAL_IP"
echo "token=$ACCESS_TOKEN"
echo "server_name=$SERVER_NAME"
echo "morpheus_url=$MORPHEUS_URL"

##
# Web Check : Build and make call
##
CHECK_NAME="Web Check [$SERVER_NAME]"
CHECK_URL="http://$EXTERNAL_IP:80"

curl -k -XPOST "$MORPHEUS_URL/api/monitoring/checks" \
  -H "Authorization: BEARER $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{'check':{
    'name': '$CHECK_NAME',
    'checkType': {'code': 'webGetCheck'},
    'inUptime': true,
    'severity': 'critical',
    'description': null,
    'checkInterval': 300,
    'checkAgent': null,
    'active': true,
    'config': {
      'webMethod': 'GET',
      'webUrl': '$CHECK_URL'
    }
  }}"