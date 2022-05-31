import time

SECONDS_TO_WAIT = {{ SECONDS_TO_WAIT }}

def run(job, **kwargs):
    job.set_progress("Pausing job for {} seconds.".format(SECONDS_TO_WAIT))
    time.sleep(SECONDS_TO_WAIT)
    return '', '', ''