"""
Plugin: Upload Files to S3 Bucket
"""

import os
import boto3
from botocore.exceptions import ClientError
from common.methods import set_progress
from infrastructure.models import Environment
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

    # 2. Stage files to upload
    set_progress("Moving files locally...")
    os.system("git clone https://github.com/jjbrassa/cb-tools.git /tmp/cb-tools")

    # 3. Connect to bucket
    set_progress("Connecting to Amazon S3... rh[" + rh_id + "] region[" + region + "]")
    rh = AWSHandler.objects.get(id=rh_id)
    s3_client = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=rh.serviceaccount,
        aws_secret_access_key=rh.servicepasswd
    )

    # 4. Upload files
    set_progress("START: Moving files Amazon S3...")
    set_progress("Moving files into bucket [" + s3_bucket_name + "]...")
    try:
        for entry in os.scandir("/tmp/cb-tools/app-samples/HTTP-App"):
            set_progress("Uploading file[" + entry.name + "]")
            response = s3_client.upload_file(entry.path, s3_bucket_name, entry.name)
    except ClientError as ce:
        logger.error(ce)

    # 5. Cleanup!
    set_progress("FINISH: Moving files Amazon S3...")
    os.system("rm -rf /tmp/cb-tools")

    if True:
        return "SUCCESS", "Files moved to S3 Bucket successfully", ""
    else:
        return "FAILURE", "Failure moving files to S3 Bucket"