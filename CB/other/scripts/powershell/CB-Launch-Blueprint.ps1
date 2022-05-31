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
   'username' = '<# username #>'
   'password' = '<# password #>'
}
 
$Parameters = @{
    Method = "Post"
    Uri =  "https://<# appliance url #>/api/v2/api-token-auth/"
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
                "blueprint": "/api/v2/blueprints/BP-ammouvoq/",
                "blueprint-items-arguments": {
                    "build-item-Server": {
                        "attributes": {
                            "hostname": "jeffb-from-api-yo",
                            "quantity": 1
                        },
                        "environment": "/api/v2/environments/ENV-zsxxio85/",
                        "os-build": "/api/v2/os-builds/OSB-54avjkl3/",
                        "parameters": {
                            "app-name": "App Server",
                            "cost-center": "Finance",
                            "ebs-volume-type": "gp2",
                            "hostname-template": "jeffb-from-api-yo",
                            "instance-type": "t3.nano",
                            "key-name": "cb-jbrassard",
                            "sc-nic-0": "subnet-5a2de63f",
                            "sec-groups": [
                                "default"
                            ],
                            "service-tier": "24x7x7"
                        }
                    }
                },
                "resource-name": "",
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
    Uri =  "https://<# appliance url #>/api/v2/orders/"
    ContentType = "application/json"
    Headers = $Headers2
    Body = $BPCreate
}

Invoke-RestMethod -SkipCertificateCheck @Parameters2


