#!/bin/bash
#
# Retrieves an instances based on instance name
#

INSTANCE_NAME="jb-tomcat-1003"

# 1. Auth
ACCESS_TOKEN=$(curl -k -X POST --data "username=$MORPHEUS_USERNAME&password=$MORPHEUS_PASSWORD" "https://10.30.20.17/oauth/token?grant_type=password&scope=write&client_id=morph-customer" | jq '.access_token') 

echo $ACCESS_TOKEN

# 2. Get List
INSTANCES=$(curl -k -X GET "https://10.30.20.180//api/instances" -H "Authorization: BEARER $ACCESS_TOKEN}" | jq '.instances[]')

# 3. Find instance


# 4. Print instance IP

## THE END ##
#echo ""$IP_ADDRESS