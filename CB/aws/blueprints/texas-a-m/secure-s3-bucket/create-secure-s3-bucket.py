"""
Plugin: Create secure s3 bucket
"""

import boto3
from common.methods import set_progress
from resourcehandlers.aws.models import AWSHandler
from infrastructure.models import CustomField
from utilities.logger import ThreadLogger

logger = ThreadLogger(__name__)

###
# RH Dropdown
###
def generate_options_for_aws_rh(server=None, **kwargs):
    options = []
    for rh in AWSHandler.objects.all():
        options.append((rh.id, rh.name))
    return sorted(options, key=lambda tup: tup[1].lower())

###
# Region Dropdown
###
def generate_options_for_s3_region(server=None, **kwargs):
    options = []
    for region in boto3.session.Session().get_available_regions('s3'):
        label = region[:2].upper() + region[2:].title()
        options.append((region, label.replace('-', ' ')))
    return sorted(options, key=lambda tup: tup[1].lower())

###
# Creates custom fields
###
def create_custom_fields():
    CustomField.objects.get_or_create(
        name='aws_rh_id',
        defaults={'type': 'STR',
                  'label': 'AWS RH ID',
                  'description': 'Resource handler ID for Resource handler being used to connect to AWS'
                  })

###
# Main Run Method
###
def run(job, *args, **kwargs):

    # 1. Setup
    rh_id = '{{ aws_rh }}'
    region = '{{ s3_region }}'
    s3_bucket_name = '{{ s3_bucket_name_input }}'
    create_custom_fields()

    # 2. Create S3 client
    set_progress("Connecting to Amazon S3... rh["+rh_id+"] region["+region+"]")
    rh = AWSHandler.objects.get(id=rh_id)
    s3_client = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=rh.serviceaccount,
        aws_secret_access_key=rh.servicepasswd
    )

    resource = kwargs.pop('resources').first()
    resource.name = s3_bucket_name
    # Store bucket name and region on this resource as attributes
    resource.s3_bucket_name = s3_bucket_name
    resource.s3_bucket_region = region
    # Store the resource handler's ID on this resource so the teardown action
    # knows which credentials to use.
    resource.aws_rh_id = rh.id
    resource.save()

    # 3. Create the bucket
    response = s3_client.create_bucket(
        ACL='private',
        Bucket=s3_bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )
    set_progress("S3 Bucket created ["+s3_bucket_name+"]")

    # 4. Enable Versioning
    set_progress("S3 Bucket - Enable versioning...")
    s3_client.put_bucket_versioning(Bucket=s3_bucket_name, VersioningConfiguration={'Status': 'Enabled'})

    # 5. Enable Encryption
    set_progress("S3 Bucket - Enable Encryption...")
    ssec = {
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                },
            },
        ]
    }
    s3_client.put_bucket_encryption(Bucket=s3_bucket_name, ServerSideEncryptionConfiguration=ssec)

    # 6. Enable Logging
    set_progress("S3 Bucket - Enable Logging...")
    bls = {
        'LoggingEnabled': {
            'TargetBucket': 'cb-server-access-logging',
            'TargetPrefix': 'cloudbolt'
        }
    }
    s3_client.put_bucket_logging(Bucket=s3_bucket_name, BucketLoggingStatus=bls)

    # 7. Add a Policy
    #aPolicy = {
    #    "Version": "2012-10-17",
    #    "Statement": [
    #        {
    #            "Sid": "Stmt1621301970069",
    #            "Effect": "Deny",
    #            "Principal": "*",
    #            "Action": "s3:*",
    #            "Resource": "arn:aws:s3:::"+s3_bucket_name+"/*"
    #        }
    #    ]
    #}
    #set_progress("S3 Bucket - Adding a policy...")
    #s3_client.put_bucket_policy(Bucket=s3_bucket_name, Policy=aPolicy)

    pabc = {
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    }
    s3_client.put_public_access_block(Bucket=s3_bucket_name, PublicAccessBlockConfiguration=pabc)

    if True:
        return "SUCCESS", "Created S3 Bucket Successfully", ""
    else:
        return "FAILURE", "Failure creating S3 Bucket"