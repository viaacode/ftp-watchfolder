import hashlib
import logging

__author__ = 'viaa'


def generate_md5(file_path):
    try:
        logging.debug("Generating MD5")
        md5 = hashlib.md5()
        with open(file_path,'rb') as f:
            for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as ex:
        logging.error("Could not generate md5 for " + file_path + "(" + type(ex).__name__ + ")")