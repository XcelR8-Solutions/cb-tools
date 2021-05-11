"""
Plugin: Get SecurityGroups For Env
"""

from infrastructure.models import Environment
from resourcehandlers.aws.models import AWSHandler
from utilities.logger import ThreadLogger

logger = ThreadLogger(__name__)


###
# Subnets
###
def get_options_list(field, profile, control_field=None, control_value=None, server=None, **kwargs):
    env_sgs = []
    try:
        env = Environment.objects.get(id=control_value)
        region = env.aws_region
        rh = AWSHandler.objects.get(id=env.resource_handler.id)
        ec2 = rh.get_boto3_client(region_name=region)
        response = ec2.describe_security_groups()
        if response.get('SecurityGroups'):
            for sg in response['SecurityGroups']:
                env_sgs.append(
                    (sg['GroupId'], sg['GroupName'],),
                )
    except Exception as ex:
        logger.error(ex)

    return env_sgs