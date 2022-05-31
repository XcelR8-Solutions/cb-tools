"""
RUN : Adds a node (new VM) to SolarWinds Monitoring

Pre-reqs:
-------------
1. A connection object to your SolarWinds instance (example code name = SolarWinds - LAB)
2. Installation of the orionsdk on your appliance (pip install orionsdk)

Details:
-------------


"""
from common.methods import set_progress
from orionsdk import SwisClient
from utilities.exceptions import CloudBoltException
from utilities.models import ConnectionInfo
from infrastructure.models import Server

SOLAR_WINDS_CONN = 'SolarWinds - LAB'

###
# Retrieves a connection object to SolarWinds
###
def get_swis_client():
    # Get SolarWinds ConnectionInfo
    conn = ConnectionInfo.objects.get(name=SOLAR_WINDS_CONN)
    if not conn:
        raise CloudBoltException("Missing required SolarWinds connection info. "
                                 "(Admin -> Connection Info -> New Connection Info)")
    return SwisClient(conn.ip, conn.username, conn.password)

###
# Main Plugin Run Method
###
def run(job=None, *args, **kwargs):

    # 1. Get SolarWinds conn
    try:
        set_progress("Checking SolarWinds connection...")
        swisClient = get_swis_client()

        # 2. Assemble payload and call SolarWinds to add
        server = job.server_set.first()
        assert isinstance(server, Server)
        server_ip = server.ip
        server_hostname = server.hostname
        set_progress("Calling SolarWinds["+SOLAR_WINDS_CONN+"] to add node name["+server_hostname+"] ip["+str(server_ip)+"]")

        # LOGIC HERE
        set_progress("Finished adding node ["+server_hostname+"] to Solarwinds")

    except CloudBoltException as cbex:
        return 'WARNING', '', cbex.details

    if True:
        return "SUCCESS", "Node Added Successfully!", ""
    else:
        return "FAILURE", "Fail : Unable to add Node", "Fail : Unable to add node"