__author__ = 'root'

import os


def move_file(package, folder):
    for file_entry in package:
        new_path = file_entry.get('file_path') + "/" + folder
        os.rename(
            file_entry.get('file_path') + "/" + file_entry.get('file_name'),
            new_path + "/" + file_entry.get('file_name')
        )
        file_entry.update({'file_path': new_path})
    pass
