"""
This is a working sample CloudBolt plug-in for you to start with. The run method is required,
but you can change all the code within it. See the "CloudBolt Plug-ins" section of the docs for
more info and the CloudBolt forge for more examples:
https://github.com/CloudBoltSoftware/cloudbolt-forge/tree/master/actions/cloudbolt_plugins
"""
from common.methods import set_progress
from infrastructure.models import CustomField
from resourcehandlers.aws.models import AWSHandler
import boto3


def generate_options_for_aws_rh(server=None, **kwargs):
    options = []
    for rh in AWSHandler.objects.all():
        options.append((rh.id, rh.name))
    return sorted(options, key=lambda tup: tup[1].lower())


def create_custom_fields():
    CustomField.objects.get_or_create(
        name='aws_rh_id',
        defaults={'type': 'STR',
                  'label': 'AWS RH ID',
                  'description': 'Resource handler ID for Resource handler being used to connect to AWS'
                  })


def run(job, *args, **kwargs):
    rh_id = '{{ aws_rh }}'
    notebook_instance_name = '{{ notebook_instance_name_input }}'
    rh = AWSHandler.objects.get(id=rh_id)
    create_custom_fields()

    set_progress("Connection to Amazon Sagemaker...")
    client = boto3.client(
        'sagemaker',
        region_name='us-west-1',
        aws_access_key_id=rh.serviceaccount,
        aws_secret_access_key=rh.servicepasswd
    )

    set_progress("Creating Sagemaker notebook instance - {}".format(notebook_instance_name))
    response = client.create_notebook_instance(
        NotebookInstanceName=notebook_instance_name,
        InstanceType='ml.t2.large',
        SubnetId='subnet-5a2de63f',
        SecurityGroupIds=[
            'sg-77924512',
        ],
        RoleArn='arn:aws:iam::486888425288:role/service-role/AmazonSageMaker-ExecutionRole-20210324T085177',
    )
    if True:
        return "SUCCESS", "Sucessfully created new Sagemaker notebook instance", ""
    else:
        return "FAILURE", "Failure creating Sagemaker notebook instance"