import configparser
import logging
import logging.config
import os
import sys

import ftpwatcher
from ftpwatcher.util.daemon3x import daemon
from ftpwatcher.util.rabbit_connector import Connector

__author__ = 'viaa'


def config_logger(file_path):
    logging.basicConfig(
        filename=file_path + '/.watcher.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )


class Watcher(daemon):
    def __init__(self, pidfile):
        super().__init__(pidfile)
        self.connector = None

    def run(self):
        watching_folder = sys.argv[2]
        config = configparser.ConfigParser()
        config.read(watching_folder + "/.watcher.conf")
        default = config['DEFAULT']
        config_logger(sys.argv[2])
        self.connector = Connector(
            host=config['RABBIT_MQ_HOST'],
            port=int(config['RABBIT_MQ_PORT']),
            username=config['RABBIT_MQ_USER'],
            password=config['RABBIT_MQ_PASSWORD'],
            exchange=config['RABBIT_MQ_SUCCESS_EXCHANGE'],
            topic_type=config['RABBIT_MQ_TOPIC_TYPE'],
            queue=config['RABBIT_MQ_SUCCESS_QUEUE'],
            routing_key=config['FLOW_ID']
        )
        ftpwatcher.watch_folder(sys.argv[2], default, self.connector)

    def stop(self):
        self.connector.close_connection()
        super().stop()


def print_error(message):
    print(message)
    sys.exit(2)


def validate_args():
    if not len(sys.argv) == 3:
        print_error("usage: python3 watcher.py [start|stop|restart] [directory_path]")

    if not os.path.isdir(sys.argv[2]):
        print_error(sys.argv[2] + " is not a directory or does not exist")

    if not os.path.exists(sys.argv[2] + '/.watcher.conf'):
        print_error('No config file found. Please place the config file in the given directory')
    pass


if __name__ == "__main__":
        validate_args()
        watcher = Watcher(sys.argv[2] + '/.watcher.pid')
        if 'start' == sys.argv[1]:
                watcher.start()
        elif 'stop' == sys.argv[1]:
                watcher.stop()
        elif 'restart' == sys.argv[1]:
                watcher.restart()
        else:
                print_error("usage: python3 watcher.py [start|stop|restart] [directory_path]")
        sys.exit(0)
