from common.methods import set_progress


def run(job, server, **kwargs):
    if server.enable_monitoring:
        server.tags.add('monitor')
        
    return "SUCCESS", "", ""