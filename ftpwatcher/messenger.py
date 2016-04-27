import logging

from ftpwatcher.util import file_util, message_generator


def send_message(package, config, rabbit_connector):
    logging.info("Processing package...")
    file_util.move_file(package, config['PROCESSING_FOLDER_NAME'])
    rabbit_connector.send_message(
            message=message_generator.create_mq_message(package.files, config)
    )


def send_error_message(package, config, rabbit_connector):
    logging.info("Processing package...")
    file_util.move_file(package, config['INCOMPLETE_FOLDER_NAME'])
    rabbit_connector.send_message(
        message=message_generator.create_mq_message(package.files, config)
    )
