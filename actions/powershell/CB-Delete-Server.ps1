echo "--------------------------------------------------"
echo "CloudBolt REST API Delete Server Example!"
echo "--------------------------------------------------"

###
# 1. Auth and get bearer token
###
echo "Auth against API..."
$Headers = @{
    'Accept' = 'application/json'
    'Content-Type' = 'application/json'
}

$Body = @{
   'username' = 'jbrassard'
   'password' = 'D00kie4me!!'
}
 
$Parameters = @{
    Method = "Post"
    Uri =  "https://cloudbolt-local.com/api/v2/api-token-auth/"
    Body = ($Body | ConvertTo-Json) 
    ContentType = "application/json"
    Headers = $Headers
}

$Response = Invoke-RestMethod -SkipCertificateCheck @Parameters
$BearerToken = $Response.token

###
# 2. Hit API and delete server
###
echo "Calling API To Delete Server..."
$OrderDelete = @'
{
    "group": "/api/v2/groups/GRP-4ocssk7c/",
    "items": {
        "decom-items": [
            {
                "environment": "/api/v2/environments/ENV-zsxxio85/",
                "servers": [
                    "/api/v2/servers/3255"
                ]
            }
        ]
    }
}
'@

$Headers2 = @{
    'Accept' = 'application/json'
    'Content-Type' = 'application/json'
    'Authorization' = "Bearer $BearerToken"
}

$Parameters2 = @{
    Method = "Post"
    Uri =  "https://cloudbolt-local.com/api/v2/orders/"
    ContentType = "application/json"
    Headers = $Headers2
    Body = $OrderDelete
}

$Response = Invoke-RestMethod -SkipCertificateCheck @Parameters2

$Response.items
$Response._links


