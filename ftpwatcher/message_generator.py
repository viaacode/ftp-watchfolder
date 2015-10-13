import json


def create_mq_message(package, config):
    return json.dumps({
        "cp_name": config['CP'],
        "flow_id": config['FLOW_ID'],
        "server": config['FTP_SERVER'],
        "username": config['FTP_USERNAME'],
        "password": config['FTP_PASSWORD'],
        "sid_package": package
    })
