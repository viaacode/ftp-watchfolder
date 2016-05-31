import logging
import time

from ftpwatcher.messenger import send_message
from ftpwatcher.util.file_util import move_file


def loop(file_index, config):
    not_gonna_give_you_up = True
    max_nr_of_checks = int(config['CHECK_PACKAGE_AMOUNT'])
    while not_gonna_give_you_up:
        logging.info('Checking file_index on completed packages...')
        keys = file_index.packages.keys()
        for package_name in keys:
            try:
                package = file_index.packages.get(package_name)
                if is_package_complete(package, config):
                    logging.info('Package \'{}\' complete.'.format(package_name))
                    process_package(file_index, package_name, config['PROCESSING_FOLDER_NAME'], config)
                elif package.reached_max_checks(max_nr_of_checks):
                    logging.info('Package \'{}\' considered incomplete. Maximum checks reached.'.format(package_name))
                    move_file(package, config['INCOMPLETE_FOLDER_NAME'])
                    file_index.remove_package(package_name)
                else:
                    package.increment_times_checked()
                    logging.info('Package {} is still incomplete. Check {} of {}'.format(package_name, package.times_checked, max_nr_of_checks))
            except Exception as ex:
                logging.error('Checking file_index failed: {}'.format(str(ex)))
        logging.info('{} incomplete packages remaining...'.format(len(file_index.packages)))
        time.sleep(int(config['CHECK_PACKAGE_INTERVAL']))


def process_package(file_index, package_name, destination_folder, config):
    try:
        logging.info('Processing package: {}'.format(package_name))
        package = file_index.packages.get(package_name)
        move_file(package, destination_folder)
        send_message(package, config)
        file_index.remove_package(package_name)
        logging.info('Package processed: {}'.format(package_name))
    except Exception as ex:
        logging.critical("Processing Package {} failed! ExceptionType: {}, Message: {}".format(package_name, type(ex).__name__, str(ex)))


def is_package_complete(package, config):
    has_essence = False
    has_sidecar = False
    has_collateral = False

    for entry in package.files:
        file_type = entry.get("file_type")
        if file_type == "essence":
            has_essence = True
        elif file_type == "sidecar":
            has_sidecar = True
        elif file_type == "collateral":
            has_collateral = True

    if config['COLLATERAL_FILE_TYPE']:
        return has_essence and has_sidecar and has_collateral
    else:
        return has_essence and has_sidecar
