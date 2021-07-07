echo "--------------------------------------------------"
echo "CloudBolt REST API Blueprint Example!"
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
# 2. Hit API and fire up workload!
###
echo "Calling API To Create BluePrint..."
$BPCreate = @'
{
    "group": "/api/v2/groups/GRP-4ocssk7c/",
    "items": {
        "deploy-items": [
            {
                "blueprint": "/api/v2/blueprints/BP-df7476du/",
                "blueprint-items-arguments": {
                    "build-item-Ubuntu-18.04-Build": {
                        "attributes": {
                            "quantity": 1
                        },
                        "environment": "/api/v2/environments/ENV-zsxxio85/",
                        "os-build": "/api/v2/os-builds/OSB-2qeptzs2/",
                        "parameters": {
                            "app-name": "App Server",
                            "cost-center": "Finance",
                            "service-tier": "24x7x7"
                        }
                    }
                },
                "resource-name": "ubuntu1804",
                "resource-parameters": {}
            }
        ]
    },
    "submit-now": "true"
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
    Body = $BPCreate
}

Invoke-RestMethod -SkipCertificateCheck @Parameters2


