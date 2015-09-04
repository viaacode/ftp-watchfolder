import hashlib
import logging

__author__ = 'viaa'


def generate_md5(file_path):
    try:
        logging.debug("Generating MD5")
        with open(file_path, 'rb') as file_to_check:
            # read contents of the file
            data = file_to_check.read()
            # pipe contents of the file through
            return hashlib.md5(data).hexdigest()
    except Exception as ex:
        logging.error("Could not generate md5 for " + file_path + "(" + type(ex).__name__ + ")")
