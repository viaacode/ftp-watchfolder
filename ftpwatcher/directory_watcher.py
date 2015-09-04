__author__ = 'viaa'

import pyinotify
import time
import logging
import datetime


def watch(directory_path, file_index_instance):
    logging.debug("Starting watcher for directory: " + directory_path)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler(file_index_instance))
    wm.add_watch(directory_path, mask=pyinotify.IN_CLOSE_WRITE)
    notifier.loop()


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, file_index_instance, **kargs):
        super().__init__(**kargs)
        self.file_index = file_index_instance

    def get_time(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def process_IN_CLOSE_WRITE(self, event):
        if not event.dir:
            self.file_index.add_file(file_path=event.path, file_name=event.name)
            logging.debug(self.get_time() + ": Received a new file - " + event.name)
