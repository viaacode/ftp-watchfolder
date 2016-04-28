import re


def match_to_regex(file_names, allowed_filetypes):
    if allowed_filetypes:
        parsed_allowed_filetypes = allowed_filetypes.replace(".", '\.')
        # File has to end with the configured extension.
        regex = ".*\.(" + parsed_allowed_filetypes + ")$"
        return re.compile(regex).match(file_names)
    else:
        return False


def is_collateral(file_name, config):
    return match_to_regex(file_names=file_name, allowed_filetypes=config['COLLATERAL_FILE_TYPE'])


def is_sidecar(file_name, config):
    return match_to_regex(file_names=file_name, allowed_filetypes=config['SIDECAR_FILE_TYPE'])


def is_essence(file_name, config):
    return match_to_regex(file_names=file_name, allowed_filetypes=config['ESSENCE_FILE_TYPE'])
