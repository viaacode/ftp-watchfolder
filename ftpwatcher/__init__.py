from ftpwatcher.fileindex import FileIndex
from ftpwatcher import directory_watcher


def watch_folder(folder_path, config):
    file_index = FileIndex(config)
    directory_watcher.watch(folder_path, file_index, config)
