import logging
import logging.config
import os
import sys
import configparser
import ftpwatcher
from ftpwatcher.daemon3x import daemon

__author__ = 'viaa'


def config_logger(file_path):
    logging.basicConfig(
        filename=file_path + '/.watcher.log',
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )


class Watcher(daemon):
    def run(self):
        watching_folder = sys.argv[2]
        config = configparser.ConfigParser()
        config.read(watching_folder + "/.watcher.conf")
        default = config['DEFAULT']
        config_logger(sys.argv[2])
        ftpwatcher.watch_folder(sys.argv[2], default)


"""if __name__ == "__main__":
    watching_folder = sys.argv[2]
    config = configparser.ConfigParser()
    config.read(watching_folder + "/.watcher.conf")
    default = config['DEFAULT']
    config_logger(sys.argv[2])
    ftpwatcher.watch_folder(sys.argv[2], default)"""


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
