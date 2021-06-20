"""
Plugin: SageMaker!
https://github.com/CloudBoltSoftware/cloudbolt-forge/tree/master/actions/cloudbolt_plugins
"""
from common.methods import set_progress
from infrastructure.models import CustomField, Environment
from resourcehandlers.aws.models import AWSHandler
import boto3


###
# AWS Environment Dropdown
###
def generate_options_for_aws_environment(profile=None, **kwargs):
    envs_this_user_can_view = Environment.objects_for_profile(profile)
    aws_handlers = AWSHandler.objects.all()
    aws_envs = envs_this_user_can_view.filter(resource_handler_id__in=aws_handlers)
    envs = [('', 'Select an Environment')]
    for env in aws_envs:
        envs.append((env.id, env.name))
    return envs


###
# Subnet Dropdown
###
def generate_options_for_subnet(profile=None, **kwargs):
    return []


###
# Security Group
###
def generate_options_for_securitygroup(profile=None, **kwargs):
    return []


###
# Role
###
def generate_options_for_role(profile=None, **kwargs):
    return []


###
# Main Run Method
###
def run(job, *args, **kwargs):
    env = Environment.objects.get(id='{{ aws_environment }}')
    subnet = '{{ subnet }}'
    securitygroup = '{{ securitygroup }}'
    role = '{{ role }}'
    notebook_instance_name = '{{ notebook_instance_name_input }}'
    rh = AWSHandler.objects.get(id=env.resource_handler.id)

    set_progress("Connection to Amazon Sagemaker...")

    client = boto3.client(
        'sagemaker',
        region_name=env.aws_region,
        aws_access_key_id=rh.serviceaccount,
        aws_secret_access_key=rh.servicepasswd
    )

    set_progress("Creating Sagemaker notebook instance - {}".format(notebook_instance_name))

    response = client.create_notebook_instance(
        NotebookInstanceName=notebook_instance_name,
        InstanceType='ml.t2.large',
        SubnetId=subnet,
        SecurityGroupIds=[
            securitygroup,
        ],
        RoleArn=role,
    )

    if True:
        return "SUCCESS", "Sucessfully created new Sagemaker notebook instance", ""
    else:
        return "FAILURE", "Failure creating Sagemaker notebook instance"