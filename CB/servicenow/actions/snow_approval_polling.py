import requests
import cbhooks
from itsm.servicenow.models.servicenow_itsm import ServiceNowITSM
from django.utils.http import urlencode
from common.methods import set_progress
from orders.models import Order, get_current_time, ActionJobOrderItem
from django.contrib.auth.models import User
from utilities.exceptions import CloudBoltException
from django.utils.html import escape, format_html
from jobs.models import Job
from django.utils.translation import ugettext as _


"""
    ServiceNow Service Request Queue
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    This one was designed to work with the ITSM SNOW integration

    Created By: Steven Manross (CloudBolt)
"""


def run(job=None, logger=None, **kwargs):
    set_progress('Running ServiceNow Request queue manager')

    # Get all PENDING orders that have ServiceNow sys_ids atached
    pending_orders = Order.objects.filter(status='PENDING', orderitem__blueprintorderitem__isnull=False, orderitem__blueprintorderitem__custom_field_values__field__name='snow_order_submit_sys_id')
    if not pending_orders:
        return "SUCCESS", "There were no pending orders waiting on ServiceNow approvals", ""

    snowitsm = ServiceNowITSM.objects.first()  # there's likely only one
    # snowitsm = ServiceNowITSM.objects.get(name='somename')  # but you can specify a specific one like this
    wrapper = snowitsm.get_api_wrapper()
    base_url = wrapper.service_now_instance_url.replace("/login.do", "")

    """
    Loop through pending orders which have a PENDING status.
    Update status to be the status which has been set in ServiceNow
    """

    for order in pending_orders:
        set_progress(f'SNOW pending order: {order.id} -> {order.status}')
        bpoi = order.orderitem_set.filter(blueprintorderitem__isnull=False, blueprintorderitem__custom_field_values__field__name='snow_order_submit_sys_id').first().cast()
        cfv = bpoi.custom_field_values.filter(field__name='snow_order_submit_sys_id').first()
        set_progress(f'&nbsp;&nbsp;&nbsp;&nbsp;Getting approval status for order # ({order.id}) for SNOW request_id: {cfv.str_value}')
        approval_data = lookup_ci(table_name='sc_request',
                                  ci_name='sys_id',
                                  ci_value=cfv.str_value,
                                  base_url=base_url,
                                  return_ci=['number', 'stage'],
                                  conn=snowitsm)

        set_progress('&nbsp;&nbsp;&nbsp;&nbsp;SNOW approval state: {}'.format(approval_data['stage']))
        if approval_data['stage'] == 'delivery':
            '''
            # leave this out for now because we want to handle this in a later release
            # (no approver data is currently available in the SNOW request output)
            approver_data = lookup_ci(table_name='sys_user',
                                      ci_name='sys_id',
                                      ci_value=approval_data['approver']['value'],
                                      base_url=base_url,
                                      sysparm_query=False,
                                      return_ci=['email', 'first_name', 'last_name', 'user_name'],
                                      conn=snowitsm)

            approve_order(approver_data, order)
            '''
            approve_order({}, order)
        else:
            set_progress(f"&nbsp;&nbsp;&nbsp;&nbsp;Order was not approved in ServiceNow:Order ID: {order.id} --> state: {approval_data['stage']}")

    return "SUCCESS", "", ""


def approve_order(approver_data, order):
    '''
    approver, created = User.objects.get_or_create(email=approver_data['email'],
                                                   defaults={"username": approver_data['user_name'],
                                                             "first_name": approver_data['first_name'],
                                                             "last_name": approver_data['last_name']})

    '''
    approver, created = User.objects.get_or_create(email="servicenow-cloudbolt@ab-inbev.com",
                                                   defaults={"username": "service-now-cloudbolt@ab-inbev.com",
                                                             "first_name": "Service",
                                                             "last_name": "Now"})

    profile = approver.userprofile
    order.approved_by = profile
    order.approved_date = get_current_time()
    order.status = 'ACTIVE'
    order.save()

    history_msg = f"The '{order}' has been approved through ServiceNow by: {profile.user.get_full_name()}"
    order.add_event("APPROVED", history_msg, profile=profile)

    try:
        cbhooks.run_hooks("pre_order_execution", order=order)
    except cbhooks.exceptions.HookFailureException as e:
        order.status = "FAILURE"
        order.save()
        msg = _(
            f"Failed to run hook for order approval. Status: {e.status},"
            f" Output: {e.output}, Errors: {e.errors}"
        )

        history_msg = _(f"The '{escape(order)}' order has failed.")

        order.add_event("FAILED", history_msg, profile=profile)
        raise CloudBoltException(msg)

    if order.status == "PENDING" and order.approvers.exists():
        link = format_html(
            f"<a href='{order.get_absolute_url()}'>{order}</a>"
        )
        msg = format_html(
            _(
                f"{link} was approved, and then marked as 'Pending' by a 'Post-Order Approval' Orchestration Action."
            ),
        )
        return [], msg

    parent_job = None

    # Saving job objects will cause them to be kicked off by the
    # job engine within a minute
    jobs = []
    order_items = [oi.cast() for oi in order.orderitem_set.filter()]
    for order_item in order_items:
        jobtype = getattr(order_item, "job_type", None)
        if not jobtype:
            # the job type will default to the first word of the class type
            # ex. "provision", "decom"

            jobtype = str(order_item.real_type).split(" ", 1)[0]
        quantity = 1

        # quantity is a special field on order_items.  If an
        # order_item has the quantity field, kick off that many
        # jobs
        if (
            hasattr(order_item, "quantity")
            and order_item.quantity is not None
            and order_item.quantity != ""
        ):
            quantity = int(order_item.quantity)
        for i in range(quantity):
            job = Job(
                job_parameters=order_item,
                type=jobtype,
                owner=order.owner,
                parent_job=parent_job,
            )
            job.save()

            # Associate the job with any server(s)
            # This may seem unnecessary because it's done when most jobs
            # run, but it's needed at the very least for scheduled server
            # modification jobs (for changing resources) so they show up on
            # the server as scheduled before they actually run

            # Since ActionJobOrderItem can contain just a resource and not
            # a server, we need to have extra logic here
            if isinstance(order_item, ActionJobOrderItem):
                if order_item.server:
                    servers = [order_item.server]
            else:
                servers = []
                if hasattr(order_item, "server"):
                    servers = [order_item.server]
                elif hasattr(order_item, "servers"):
                    servers = order_item.servers.all()
                for server in servers:
                    server.jobs.add(job)

            jobs.append(job)

    # If it didn't make any jobs, just call it done
    if not jobs:
        order.complete("SUCCESS")

    msg = 'order complete'
    set_progress(f"&nbsp;&nbsp;&nbsp;&nbsp;Order approved: {order.id}")
    return jobs, msg


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