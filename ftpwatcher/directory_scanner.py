__author__ = 'viaa'

import os
import logging


def scan(directory_path, file_index):
    logging.info("Scanning folder: " + directory_path)
    if os.path.isdir(directory_path):
        for file in os.listdir(directory_path):
            logging.info("Found file: " + file)
            file_index.add_file(file_name=file, file_path=directory_path)
