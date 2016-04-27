import logging
import time

from ftpwatcher.messenger import send_message, send_error_message


def loop(file_index, config):
    never_gonna_give_you_up = True
    max_nr_of_checks = int(config['CHECK_PACKAGE_AMOUNT'])
    while never_gonna_give_you_up:
        for index_name, package in file_index:
            if is_package_complete(package, config):
                logging.info('Package \'{}\' complete.'.format(index_name))
                send_message(package, config)
            elif package.reached_max_checks(max_nr_of_checks):
                logging.info('Package \'{}\' considered incomplete. Maximum checks reached.'.format(index_name))
                send_error_message(package, config)
            package.increment_times_checked()
            logging.info('Package {} is still incomplete. Check {} of {}'.format(index_name, package.times_checked,
                                                                                 max_nr_of_checks))
        time.sleep(int(config['CHECK_PACKAGE_INTERVAL']))


def is_package_complete(package, config):
    has_essence = False
    has_sidecar = False
    has_collateral = False

    for entry in package:
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
