from threading import Thread
from ftpwatcher import package_analyzer

import pyinotify
import time
import logging
import datetime
import threading


def watch(directory_path, file_index, config):
    logging.info("Starting watcher for directory: " + directory_path)
    wm = pyinotify.WatchManager()
    masktypes = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO | pyinotify.IN_DELETE
    notifier = pyinotify.Notifier(wm, EventHandler(file_index))
    wm.add_watch(directory_path, mask=masktypes)
    thread = Thread(target=package_analyzer.loop, args=(file_index, config), name="Thread-" + str(threading.active_count()))
    thread.start()
    logging.info("Running threads: {}".format(str(threading.active_count())))
    notifier.loop()


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, file_index_instance, **kargs):
        super().__init__(**kargs)
        logging.info("Initializing EventHandler")
        self.file_index = file_index_instance

    def get_time(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def add_to_index(self, event):
        logging.info("Adding to index")
        if not event.dir:
            self.file_index.add_file(file_path=event.path, file_name=event.name)
            logging.info("{}: Received a new file - {}".format(threading.current_thread().name, self.get_time(), event.name))

    def remove_from_index(self, event):
        logging.info("Removing from index")
        if not event.dir:
            self.file_index.remove_file(event.name)
            logging.info("{}: File {} was deleted/moved from directory.".format(threading.current_thread().name, self.get_time(), event.name))

    def process_IN_CLOSE_WRITE(self, event):
        logging.info("Received CLOSE_WRITE event")
        self.add_to_index(event)

    def process_IN_MOVED_TO(self, event):
        logging.info("Received IN_MOVED_TO event")
        self.add_to_index(event)

    def process_IN_DELETE(self, event):
        logging.info("Received IN_DELETE event")
        self.remove_from_index(event)
