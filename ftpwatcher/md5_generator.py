import hashlib
import logging

__author__ = 'viaa'


def generate_md5(file_path):
    logging.debug("Generating MD5")
    try:
        hash = hashlib.md5()
        with open(file_path, "r", encoding='utf-8') as f:
            for chunk in iter(lambda: f.read(4096), ""):
                hash.update(chunk.encode('utf-8'))
        return hash.hexdigest()
    except Exception as ex:
        logging.error("Could not generate md5 for: " + file_path + ". (" + type(ex).__name__ + ")")
