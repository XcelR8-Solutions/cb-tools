"""
RUN : Will kick off a Jenkins pipeline via a REST call
TARGET: <your jenkins server here>
"""
from common.methods import set_progress
import requests


def run(job, *args, **kwargs):

    # define vars
    jenkins_url = "http://jenkins.local:8080/job/CBTestPipeline/build?token="
    jenkins_pipeline_token = "zeFo6RhMGhWqQ9JNe7O5"
    jenkins_user = "jbrassard"
    jenkins_api_key = "11e36839bca74ad6973e9b01bb9bc51aaa"

    # Disable ssl warnings (for my example)
    requests.packages.urllib3.disable_warnings()

    # 1. Assemble Url and call jenkins
    url = jenkins_url+jenkins_pipeline_token
    set_progress("Calling Jenkins to kick build off...")
    set_progress(url)
    response = requests.get(url, auth=(jenkins_user, jenkins_api_key))
    set_progress("response="+str(response))
    set_progress("Finished kicking off build.  Check Jenkins console!")

    if True:
        return "SUCCESS", "Check : Jenkins build kicked off", ""
    else:
        return "FAILURE", "Fail : Build NOT kicked off", "Fail : Build NOT kicked off"