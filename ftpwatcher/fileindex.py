import datetime
import time
import logging
from ftpwatcher import md5_generator
from ftpwatcher import message_scheduler
from ftpwatcher import package_file_recognizer as recognizer
from threading import Thread

__author__ = 'viaa'


def get_index_name(file_name):
    return file_name.split(".")[0]


def create_file_entry(file_path, file_name, file_type):
    return {
        "file_name": file_name,
        "file_path": file_path,
        "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S'),
        "md5": "",
        "file_type": file_type
    }

class FileIndex:
    def __init__(self, config):
        self.files_in_dir = {}
        self.config = config
        self.md5_generator = md5_generator.Md5_generator(self)

    def add_file(self, file_name, file_path):
        # Only add the files determined in the ini file
        logging.info("Recognizing package file type for: " + file_name)
        file_type = recognizer.determine_file_type(file_name=file_name, config=self.config)
        if file_type is not None:
            package = []
            start_new_timer = True
            # Unique Identifier for a package
            index_name = get_index_name(file_name)
            # Generate a file entry with wanted data
            file_entry = create_file_entry(file_path=file_path, file_name=file_name, file_type=file_type)
            # Give order to generate MD5
            self.md5_generator.generate_md5(file_path, file_name)
            # If the dict already contains package files, update the list
            if index_name in self.files_in_dir:
                start_new_timer = False
                package = self.files_in_dir.get(index_name)
            # Append the new Entry
            package.append(file_entry)
            # Update dict
            self.files_in_dir.update({index_name: package})
            if start_new_timer:
                thread = Thread(target=message_scheduler.start, args=(self.files_in_dir, index_name, self.config))
                thread.start()
            logging.info("Accepted file for package handling: " + file_name)
        else:
            logging.info("Refused file for package handling: " + file_name)
        pass

    def get_package(self, file_name):
        return self.files_in_dir[file_name]
