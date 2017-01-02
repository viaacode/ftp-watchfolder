from ftpwatcher.util import message_generator, rabbit_connector
import logging


def send_message(package, config):
    logging.info("Creating connector")
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
    logging.info("Sending message using connector")
    connector.send_message(
            message=message_generator.create_mq_message(package.files, config)
    )
    logging.info("Closing connection")
    connector.close_connection()
