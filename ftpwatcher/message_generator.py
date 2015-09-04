__author__ = 'viaa'

import json


def create_mq_message(package, config):
    return json.dumps({
        "cp_name": config['CP'],
        "flow_id": config['FLOW_ID'],
        "sid_package": package
    })
