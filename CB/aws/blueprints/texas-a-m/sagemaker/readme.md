# CloudBolt AWS Sagemaker Blueprint

## Pre-reqs
AWS Environment must have a role present that has authorization to create/manage Sagemaker

## Function
This blueprint creates an AWS Sagemaker notebook instance

####Blueprint flow:
1. User is asked to choose from available list of AWS Envs
2. User specifies the Role to use
3. User specifies the Security Group to use
4. User specifies the Subnet to use
5. User specifies the Instance Size Type to use
6. User enters the notebook instance name

## Configuration
1. Map the following file to the blueprint BUILD Tab:  *sagemaker-create.py*
   1. Field Dependency:  Role Field 'Regenerate Options' => 'env_id'
   2. Field Dependency:  Security Group Field 'Regenerate Options' => 'env_id'
   3. Field Dependency:  Subnet Field 'Regenerate Options' => 'env_id'
2. Map the following file to the blueprint TEARDOWN Tab:  *sagemaker-delete.py*


