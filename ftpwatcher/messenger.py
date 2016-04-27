import logging

from ftpwatcher.util import rabbit_connector as rabbit, file_util, message_generator


def send_message(package, config):
    logging.info("Processing package...")
    file_util.move_file(package, config['PROCESSING_FOLDER_NAME'])
    rabbit.send_message(
            host=config['RABBIT_MQ_HOST'],
            port=int(config['RABBIT_MQ_PORT']),
            username=config['RABBIT_MQ_USER'],
            password=config['RABBIT_MQ_PASSWORD'],
            exchange=config['RABBIT_MQ_SUCCESS_EXCHANGE'],
            topic_type=config['RABBIT_MQ_TOPIC_TYPE'],
            queue=config['RABBIT_MQ_SUCCESS_QUEUE'],
            routing_key=config['FLOW_ID'],
            message=message_generator.create_mq_message(package.files, config)
    )


def send_error_message(package, config):
    logging.info("Processing package...")
    rabbit.send_message(
        host=config['RABBIT_MQ_HOST'],
        port=int(config['RABBIT_MQ_PORT']),
        username=config['RABBIT_MQ_USER'],
        password=config['RABBIT_MQ_PASSWORD'],
        exchange=config['RABBIT_MQ_ERROR_EXCHANGE'],
        topic_type=config['RABBIT_MQ_TOPIC_TYPE'],
        queue=config['RABBIT_MQ_ERROR_QUEUE'],
        routing_key=config['FLOW_ID'],
        message=message_generator.create_mq_message(package.files, config)
    )
    file_util.move_file(package, config['INCOMPLETE_FOLDER_NAME'])
