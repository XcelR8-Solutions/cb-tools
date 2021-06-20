"""
Plugin: Get Roles For Env
"""

from infrastructure.models import Environment
from resourcehandlers.aws.models import AWSHandler
from utilities.logger import ThreadLogger
import boto3

logger = ThreadLogger(__name__)


###
# Roles
###
def get_options_list(field, profile, control_field=None, control_value=None, server=None, **kwargs):
    roles = []

    if not control_value:
        return []

    try:
        env = Environment.objects.get(id=control_value)
        region = env.aws_region
        rh = AWSHandler.objects.get(id=env.resource_handler.id)

        iam_client = boto3.client(
            'iam',
            region_name=region,
            aws_access_key_id=rh.serviceaccount,
            aws_secret_access_key=rh.servicepasswd
        )

        response = iam_client.list_roles()
        if response.get('Roles'):
            for role in response['Roles']:
                roles.append(
                    (role['Arn'], role['RoleName'],),
                )

    except Exception as ex:
        logger.error(ex)

    return roles