"""
Selects an ENV (Environment) target based on user input

Input from user (parameters):
------------------------------
1. Location
2. App Type
3. NPI
4. Tier

Selection Logic
------------------------------
** Insert your selection logic here so it is documented

"""
from common.methods import set_progress
from infrastructure.models import Environment

RESOURCE_HANDLER_ID = 13
ENV_TARGET_1 = 'vCenter - CB-Lab-Sales LZ'
ENV_TARGET_2 = 'vCenter - CB-Lab-Sales DEV LZ'


def determine_deployment_environment_and_parameters(*args, **kwargs):
    ###
    # 1. Grab input
    ###
    env_target = ENV_TARGET_2
    location = kwargs.get('location')
    app_type = kwargs.get('app_type')
    npi = kwargs.get('npi')
    tier = kwargs.get('tier')
    set_progress("Dynamically setting VM destination based on input:")
    set_progress("-----------------------------")
    set_progress("Location [" + location + "]")
    set_progress("AppType [" + app_type + "]")
    set_progress("NPI [" + str(npi) + "]")
    set_progress("Tier [" + tier + "]")
    set_progress("-----------------------------")

    ###
    # 2. Choose ENV target based on input
    #    ** Put your env selection logic below **
    ###
    if str(location).upper() == 'HQ' or str(location).upper() == 'HQ DMZ':
        env_target = ENV_TARGET_1
    else:
        env_target = ENV_TARGET_2

    ###
    # 3. Get appropriate ENV object
    ###
    set_progress("Target ENV [" + env_target + "]")
    env = Environment.objects.get(name=env_target)

    ###
    # 4. Generate any necessary parameters
    ###
    parameters = {}

    ###
    # Return target!
    ###
    return {"environment": env, "parameters": parameters}