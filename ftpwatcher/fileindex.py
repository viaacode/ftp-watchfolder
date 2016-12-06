import datetime
import logging
import time
import threading

from os import path

from ftpwatcher.util import md5_generator
from ftpwatcher.package_file_recognizer import is_collateral, is_essence, is_sidecar
from ftpwatcher.util.package_util import get_package_name


def generate_md5(file_path, config):
    if config['MD5_CALC'] and config['MD5_CALC'].upper() == 'TRUE':
        return md5_generator.generate_md5(file_path)
    else:
        logging.info("Did not generate MD5")
        return ""


# Returns the file_type as configured (extension matches certain files), returns None if it's an invalid file
def determine_file_type(file_name, config):
    if is_essence(file_name, config):
        return "essence"
    else:
        if config['COLLATERAL_FILE_TYPE'] in config['SIDECAR_FILE_TYPE']:
            if is_sidecar(file_name, config):
                return "sidecar"
            elif is_collateral(file_name, config):
                return "collateral"
            else:
                return None
        else:
            if is_collateral(file_name, config):
                return "collateral"
            elif is_sidecar(file_name, config):
                return "sidecar"
            else:
                return None


class FileIndex:
    def __init__(self, config):
        logging.info("Initializing FileIndex")
        self.packages = {}
        self.config = config

    def add_file(self, file_name, file_path):
        # Only add the files determined in the ini file
        logging.info("Recognizing package file type for: " + file_name)
        file_type = determine_file_type(file_name, self.config)
        if file_type is not None:
            package_name = get_package_name(file_name)
            if package_name in self.packages:
                self.packages.get(package_name).add_file(file_path, file_name, file_type, self.config)
            else:
                package = Package()
                package.add_file(file_path, file_name, file_type, self.config)
                self.packages.update({package_name: package})
        else:
            logging.info("Refused file for package handling: " + file_name)

    def remove_file(self, file_name):
        logging.info("Removing self")
        package_name = get_package_name(file_name)
        package = self.packages.get(package_name)
        package.remove_file(file_name)
        if not package.has_files():
            self.remove_package(package_name)

    def remove_package(self, package_name):
        logging.info("Removing Index {}".format(package_name))
        new_index = {}
        for package_key in self.packages.keys():
            if not package_key == package_name:
                new_index.update({package_key: self.packages.get(package_key)})
        self.packages = new_index
    pass


class Package:
    def __init__(self):
        self.files = []
        self.times_checked = 0
        self.moved = False

    def add_file(self, file_path, file_name, file_type, config):
        file = list(filter(lambda file_entry: file_entry["file_name"] == file_name and file_entry["file_path"] == file_path, self.files))
        if len(file) > 0:
            logging.info("File {} was already present in the index")
        else:
            self.files.append({
                "file_name": file_name,
                "file_path": file_path,
                "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S'),
                "md5": generate_md5(path.join(file_path, file_name), config),
                "file_type": file_type
            })
            logging.info("{}: Accepted file for package handling: {}".format(threading.current_thread().name, file_name))

    def remove_file(self, file_name):
        file = list(filter(lambda file_entry: file_entry["file_name"] == file_name, self.files))
        if len(file) > 0:
            self.files.remove(file[0])
            logging.info("{} removed from index".format(file_name))
        else:
            logging.info("{} was not found in the index".format(file_name))

    def reached_max_checks(self, max_amount):
        logging.info("Reached max amount of checks!!!")
        return self.times_checked >= max_amount

    def increment_times_checked(self):
        logging.info("Increment times checked: {} with {}".format(self.times_checked, "1"))
        self.times_checked += 1

    def has_files(self):
        return len(self.files) > 0
