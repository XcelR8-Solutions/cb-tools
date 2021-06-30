#!/bin/sh
#
# Auth for web service interactions - get back bearer token
#

MORPHEUS_URL="https://10.30.20.17"

# Authenticate
AUTH_TOKEN=$(curl -k -X POST --data "username=$MORPHEUS_USERNAME&password=$MORPHEUS_PASSWORD" "$MORPHEUS_URL/oauth/token?grant_type=password&scope=write&client_id=morph-customer")
ACCESS_TOKEN=$(sed -E 's/.*"access_token":"?([^,"]*)"?.*/\1/' <<< $AUTH_TOKEN)

# Output token for task chaining
echo "access_token=$ACCESS_TOKEN,morpheus_url=$MORPHEUS_URL"