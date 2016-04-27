import datetime
import logging
import time

from os import path

from ftpwatcher.util import md5_generator
from ftpwatcher.package_file_recognizer import is_collateral, is_essence, is_sidecar


def get_package_name(file_name):
    return file_name.split(".")[0]


def generate_md5(file_path, config):
    if config['MD5_CALC'] and config['MD5_CALC'].toUpper() == 'TRUE':
        return md5_generator.generate_md5(file_path)
    else:
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
        self.packages = {}
        self.config = config

    def add_file(self, file_name, file_path):
        # Only add the files determined in the ini file
        logging.info("Recognizing package file type for: " + file_name)
        file_type = determine_file_type(file_name, self.config)
        try:
            if file_type is not None:
                package_name = get_package_name(file_name)
                if package_name in self.packages:
                    self.packages.get(package_name).add_file(file_path, file_name, file_type, self.config)
                else:
                    package = Package()
                    package.add_file(file_path, file_name, file_type, self.config)
                    self.packages.update({package_name: package})
                logging.info("Accepted file for package handling: " + file_name)
            else:
                logging.info("Refused file for package handling: " + file_name)
        except Exception as ex:
            logging.error("Could not add file to index " + file_path + "(" + type(ex).__name__ + ")")
        pass


class Package:
    def __init__(self):
        self.files = []
        self.times_checked = 0

    def add_file(self, file_path, file_name, file_type, config):
        self.files.append({
            "file_name": file_name,
            "file_path": file_path,
            "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S'),
            "md5": generate_md5(path.join(file_path, file_name), config),
            "file_type": file_type
        })

    def reached_max_checks(self, max_amount):
        return self.times_checked >= max_amount

    def increment_times_checked(self):
        self.times_checked += 1
