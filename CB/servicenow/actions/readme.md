## SNOW Actions

### ServiceNow Approvals

This plugin is highly configurable and is currently configured to insert requests into our internal dev instance of ServiceNow.  

___Environment Details:___

* Details are in the SE Confluence wiki:  https://cloudbolt.atlassian.net/wiki/spaces/SE/pages/1432617040/SovLabs+ServiceNow

___Details:___
 
* *Approval Plugin* - snow_approval.py
* *Approval Plugin Install location* -  Orchestration Actions > Order Related > III. Order Submission
* Plugin can be scoped to a specific group, environment, etc.  After scoping, it will be listed on the Group Overview page under the approvals area.
* *Approval Job Polling Plugin* - snow_approval_polling_job.py
* *Approval Job Polling Plugin Install location* -  Recurring Jobs 
 
___Approval Demonstration Instructions:___

* Details are in the SE Confluence wiki:  https://cloudbolt.atlassian.net/wiki/spaces/SE/pages/1432617040/SovLabs+ServiceNow