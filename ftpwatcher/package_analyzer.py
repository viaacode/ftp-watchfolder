__author__ = 'viaa'


def is_package_complete(package, config):
    has_essence = False
    has_sidecar = False
    has_collateral = False

    for entry in package:
        file_type = entry.get("file_type")
        if file_type == "essence" and entry.get("md5") != "":
            has_essence = True
        elif file_type == "sidecar":
            has_sidecar = True
        elif file_type == "collateral":
            has_collateral = True

    if config['COLLATERAL_FILE_TYPE']:
        return has_essence and has_sidecar and has_collateral
    else:
        return has_essence and has_sidecar
