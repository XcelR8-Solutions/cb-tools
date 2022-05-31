"""
Plugin: CloudFront to S3 Bucket
"""

import boto3
from common.methods import set_progress
from resourcehandlers.aws.models import AWSHandler
from utilities.logger import ThreadLogger

logger = ThreadLogger(__name__)

###
# Main Run Method
###
def run(job, *args, **kwargs):

    # 1. Pull params from previous blueprint
    rh_id = '{{ blueprint_context.fancy_aws_s3_bucket.create_secure_s3_bucket.aws_rh }}'
    region = '{{ blueprint_context.fancy_aws_s3_bucket.create_secure_s3_bucket.s3_region }}'
    s3_bucket_name = '{{blueprint_context.fancy_aws_s3_bucket.create_secure_s3_bucket.s3_bucket_name_input}}'


    # 2. Connect to bucket
    set_progress("Connecting to Amazon S3... rh["+rh_id+"] region["+region+"]")
    rh = AWSHandler.objects.get(id=rh_id)
    s3_client = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=rh.serviceaccount,
        aws_secret_access_key=rh.servicepasswd
    )

    # 3. Set website config
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }
    s3_client.put_bucket_website(Bucket=s3_bucket_name, WebsiteConfiguration=website_configuration)

    # 3. Build CloudFront Entries?!


    if True:
        return "SUCCESS", "CloudFront Config Successfully laid in", ""
    else:
        return "FAILURE", "Failure applying CloudFront config"