"""
Hook to add Service Catalog Request Record for Order when submitted.
Can be managed through the CloudBolt ServiceNow Management page.
"""

import json
# from datetime import datetime, timedelta
import requests
from itsm.servicenow.models.servicenow_itsm import ServiceNowITSM
from utilities.logger import ThreadLogger
from urllib.parse import urlencode
from infrastructure.models import Environment


logger = ThreadLogger("Service Now Order Submit")


def run(order, *args, **kwargs):
    """
    Creates a new service catalog request entry which will need to get approved.
    :param order: Order object
    """
    logger.info('in SNOW Approval integration.')

    if not order:
        return False

    # Find the order_item that has a reference to a servicenow request sys_id
    order_item = order.orderitem_set.filter(blueprintorderitem__isnull=False).first()

    if not order_item:
        logger.warning('No Applicable Blueorint Order Item associate with this order item: ServiceNow Service Catalog record will not be created.')
        return "FAILURE", "Blueprint Order Item not found", f"order: {order.id}"

    bp_order_item = order_item.blueprintorderitem

    snowitsm = ServiceNowITSM.objects.first()  # there's likely only one
    # snowitsm = ServiceNowITSM.objects.get(name='somename')  # but you can specify a specific one like this
    wrapper = snowitsm.get_api_wrapper()
    base_url = wrapper.service_now_instance_url.replace("/login.do", "")

    requested_by = order.owner.user.username

    snow_user_data = lookup_ci(table_name='sys_user',
                               ci_query={'user_name': requested_by},
                               base_url=base_url,
                               return_ci=['sys_id'],
                               conn=snowitsm)

    if not snow_user_data:
        logger.warning(f'Unable to find data matching order owner in ServiceNow: {requested_by} for order number: {order.id}.')
        return "FAILURE", 'Unable to find data matching order owner in ServiceNow (check snow URL?)', f'requested_by: {requested_by} --> order: {order.id}'

    sysid_for_req_by = snow_user_data['sys_id']

    if not sysid_for_req_by:
        return "FAILURE", "ServiceNow sys_id for 'requested_by' not found", requested_by

    # default to order owner
    recipient = order.owner.user.username
    sysid_for_req_for = sysid_for_req_by
    if order.recipient:
        recipient = order.recipient.user.email

        req_for_data = lookup_ci(table_name='sys_user',
                                 ci_query={'user_name': recipient},
                                 base_url=base_url,
                                 return_ci=['sys_id'],
                                 conn=snowitsm)
        if not req_for_data:
            return "FAILURE", "ServiceNow data for 'requested_for' not found", order.recipient.user.email
        sysid_for_req_for = req_for_data['sys_id']

    # this is the data structure that the request needs (for an order now catalog item)
    # customer parameter names may vary

    bpia = bp_order_item.blueprintitemarguments_set.filter(environment__isnull=False).first()
    if not bpia:
        bpia = bp_order_item
        # Terraform (and or plugins would go this route)

    # quantity = 1
    # if bpia.quantity:
    #     quantity = bpia.quantity
    request_url = f"{base_url}/api/now/table/sc_request"
    if not bpia.environment:
        # Terraform Route
        group = order.group
        env = Environment.objects.filter(resource_handler__resource_technology__name="Azure", group=group).first()
        rh = env.resource_handler
    else:
        # Server Tier Route
        rh = bpia.environment.resource_handler

    data = {"requested_by": sysid_for_req_by,
            "requested_for": sysid_for_req_for,
            "description": f'Blueprint: {order.blueprint.name}\r\nOrder: {order.id}\r\nResource handler: {rh.name}',
            }

    logger.info(f'SNOW PAYLOAD: {data}')
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    json_data = json.dumps(data)

    try:
        raw_response = wrapper.service_now_request(method="POST",
                                                   url=request_url,
                                                   headers=headers,
                                                   body=json_data)

        response = raw_response.json()
        '''
        # example response
        {'result': {'sys_id': '0f4ba4fedbc478502ebe5612f3961904',
                    'number': 'REQ0473921',
                    'request_number': 'REQ0473921',
                    'request_id': '0f4ba4fedbc478502ebe5612f3961904',
                    'table': 'sc_request'}}
        '''
        sys_id = response["result"]["sys_id"]
        request_number = response["result"]["number"]
        logger.info(f'RESPONSE: {response}')
        if not sys_id:
            raise NameError("ServiceNow sys_id not found")
        else:
            from orders.views import add_cfvs_to_order_item
            add_cfvs_to_order_item(
                bp_order_item, {"snow_order_request_number": request_number}
            )
            add_cfvs_to_order_item(
                bp_order_item, {"snow_order_submit_sys_id": sys_id}
            )
        # success
        return "", "", ""
    except Exception as e:
        return "FAILURE", f"Exception: {e}", ""


def lookup_ci(table_name=None, ci_name=None, ci_value=None, ci_query=None,
              base_url=None, return_ci='sys_id', sysparm_query=True, conn=None):
    '''
        ex.
        table_name = 'ci_cmdb_server'
        ci_name = 'asset_tag'
        ci_value = '421e19fe-5920-4ae9-75be-4646430d6772'
        return_ci = (str) or (list) (str for 1 value, list for multiple values)
                    ex. 'sys_id' or ['sys_id', 'email']
        Query servicenow with a table, and looks for a CI that has
        the field(ci_name) with the value(ci_value) and returns the sys_id for that
        CI.

        Optionally, you can pass multiple filters in the ci_query parameter as a
            dictionary...

            i.e. {'column1': 'column_value', 'column2': 'some other value'}
            ...if there is more than one filter field to query with

        If it doesn't find a record that matches the filter passed in,
           it returns None
    '''
    ci_value_data = None
    if ci_query:
        query = urlencode(ci_query)
    else:
        prefix = "sysparm_query"
        if not sysparm_query:
            query = urlencode({ci_name: ci_value})
        else:
            query = urlencode({prefix: f"{ci_name}={ci_value}"})

    url = base_url + f"/api/now/table/{table_name}?{query}"
    # print(f'lookup_ci - url: {url}')
    response = requests.get(
        url=url,
        auth=(conn.service_account, conn.password),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        timeout=5.0
    )
    # print(f'response = {response.text}')

    try:
        # if a list of values are sent for return, then populate a dictionary
        if isinstance(return_ci, list):
            ci_value_data = {}
            for item in return_ci:
                ci_value_data[item] = response.json()["result"][0][item]
        else:
            if return_ci == "*":
                # return everything we got back
                ci_value_data = response.json()["result"][0]
            else:
                ci_value_data = response.json()["result"][0][return_ci]
    except Exception:
        pass

    return ci_value_data