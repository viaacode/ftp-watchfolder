from ftpwatcher.util import message_generator, rabbit_connector


def send_message(package, config):
    connector = rabbit_connector.Connector(
            host=config['RABBIT_MQ_HOST'],
            port=int(config['RABBIT_MQ_PORT']),
            username=config['RABBIT_MQ_USER'],
            password=config['RABBIT_MQ_PASSWORD'],
            exchange=config['RABBIT_MQ_SUCCESS_EXCHANGE'],
            topic_type=config['RABBIT_MQ_TOPIC_TYPE'],
            queue=config['RABBIT_MQ_SUCCESS_QUEUE'],
            routing_key=config['FLOW_ID']
    )
    connector.send_message(
            message=message_generator.create_mq_message(package.files, config)
    )
    connector.close_connection()
