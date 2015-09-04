import hashlib

__author__ = 'viaa'


def generate_md5(file_path):
    hash = hashlib.md5()
    with open(file_path) as f:
        for chunk in iter(lambda: f.read(4096), ""):
            hash.update(chunk)
    return hash.hexdigest()