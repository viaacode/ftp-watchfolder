import logging
import time

from ftpwatcher.messenger import send_message, send_error_message


def loop(file_index, config):
    not_gonna_give_you_up = True
    max_nr_of_checks = int(config['CHECK_PACKAGE_AMOUNT'])
    while not_gonna_give_you_up:
        logging.info("Checking file_index on completed packages...")
        for index_name in file_index.packages.keys():
            try:
                package = file_index.packages.get(index_name)
                if is_package_complete(package.files, config):
                    logging.info('Package \'{}\' complete.'.format(index_name))
                    send_message(package, config)
                elif package.reached_max_checks(max_nr_of_checks):
                    logging.info('Package \'{}\' considered incomplete. Maximum checks reached.'.format(index_name))
                    send_error_message(package.files, config)
                package.increment_times_checked()
                logging.info('Package {} is still incomplete. Check {} of {}'.format(index_name, package.times_checked,
                                                                                     max_nr_of_checks))
            except Exception as ex:
                logging.error('Checking file_index failed: {}'.format(str(ex)))
        time.sleep(int(config['CHECK_PACKAGE_INTERVAL']))


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
