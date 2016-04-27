import os
import logging


def move_file(package, folder):
    for file_entry in package.files:
        new_path = os.path.join(file_entry.get('file_path'), folder)
        source = os.path.join(file_entry.get('file_path'), file_entry.get('file_name'))
        destination = os.path.join(new_path, file_entry.get('file_name'))
        logging.info("Moving '{}' to '{}'.".format(source, destination))
        os.rename(
                source,
                destination
        )
        file_entry.update({'file_path': new_path})
        logging.info("File moved.")
    pass
