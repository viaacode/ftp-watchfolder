import os
import logging


def move_file(package, folder):
    for file_entry in package.files:
        new_path = file_entry.get('file_path') + "/" + folder
        source = file_entry.get('file_path') + "/" + file_entry.get('file_name')
        destination = new_path + "/" + file_entry.get('file_name')
        logging.info("Moving '{}' to '{}'.".format(source, destination))
        os.rename(
                source,
                destination
        )
        file_entry.update({'file_path': new_path})
        logging.info("File moved.")
    pass
