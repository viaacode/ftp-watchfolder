__author__ = 'viaa'

import sched
import time
import logging
from ftpwatcher import file_util
from ftpwatcher import message_generator
from ftpwatcher import package_analyzer as analyzer
from ftpwatcher import rabbit_connector as rabbit


def send_message_if_complete(file_index, index_name, config, scheduler, counter):
    package = file_index.get(index_name)
    logging.info('Checking ' + file_index)
    if analyzer.is_package_complete(package, config):
        try:
            logging.info('Package \'{}\' complete.'.format(index_name))
            send_message(package, config)
            del file_index[index_name]
        except Exception as ex:
            logging.critical("Could not send message due to connection issues (" + type(ex).__name__ + ")")
    elif int(counter) == int(config['CHECK_PACKAGE_AMOUNT']):
        try:
            logging.info('Package \'{}\' considered incomplete. Maximum checks reached.'.format(index_name))
            send_error_message(package, config)
            del file_index[index_name]
        except Exception as ex:
            logging.critical("Could not send message due to connection issues (" + type(ex).__name__ + ")")
    else:
        logging.info('Package {} is still incomplete. Check {} of {}'.format(counter + 1, int(config['CHECK_PACKAGE_AMOUNT'])))
        add_scheduler_event(scheduler, file_index, index_name, config, counter + 1)


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
        message=message_generator.create_mq_message(package, config)
    )
    pass


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
        message=message_generator.create_mq_message(package, config)
    )
    file_util.move_file(package, config['INCOMPLETE_FOLDER_NAME'])
    pass


def start(file_index, index_name, config):
    scheduler = sched.scheduler(time.time, time.sleep)
    add_scheduler_event(scheduler, file_index, index_name, config, 1)
    scheduler.run()


def add_scheduler_event(scheduler, file_index, index_name, config, counter):
    scheduler.enter(
        delay=int(config['CHECK_PACKAGE_INTERVAL']),
        priority=1,
        action=send_message_if_complete,
        kwargs={'file_index': file_index,
                'index_name': index_name,
                'config': config,
                'scheduler': scheduler,
                'counter': counter}
    )
