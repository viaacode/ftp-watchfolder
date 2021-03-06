from ftpwatcher.fileindex import FileIndex
from ftpwatcher import directory_watcher, directory_scanner
import logging


def watch_folder(folder_path, config):
    logging.info("Watching folder {}".format(folder_path))
    file_index = FileIndex(config)
    directory_scanner.scan(folder_path, file_index)
    directory_watcher.watch(folder_path, file_index, config)
