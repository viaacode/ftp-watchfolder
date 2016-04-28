from threading import Thread
from ftpwatcher import package_analyzer

import pyinotify
import time
import logging
import datetime


def watch(directory_path, file_index, config):
    logging.info("Starting watcher for directory: " + directory_path)
    wm = pyinotify.WatchManager()
    masktypes = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO | pyinotify.IN_DELETE
    notifier = pyinotify.Notifier(wm, EventHandler(file_index))
    wm.add_watch(directory_path, mask=masktypes)
    thread = Thread(target=package_analyzer.loop, args=(file_index, config))
    thread.start()
    notifier.loop()


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, file_index_instance, **kargs):
        super().__init__(**kargs)
        self.file_index = file_index_instance

    def get_time(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def add_to_index(self, event):
        if not event.dir:
            self.file_index.add_file(file_path=event.path, file_name=event.name)
            logging.info("Received a new file - {}".format(self.get_time(), event.name))

    def remove_from_index(self, event):
        if not event.dir:
            self.file_index.remove_file(event.name)
            logging.info("File {} was deleted/moved from directory.".format(self.get_time(), event.name))

    def process_IN_CLOSE_WRITE(self, event):
        self.add_to_index(event)

    def process_IN_MOVED_TO(self, event):
        self.add_to_index(event)

    def process_IN_DELETE(self, event):
        self.remove_from_index(event)
