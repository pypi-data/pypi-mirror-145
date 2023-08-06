import logging
import json
import pickle
import os


logger = logging.getLogger(__name__)

__all__ = ['read_config_file', 'import_dictionary']


def import_dictionary(path, file):
    with open(os.path.join(path, file), 'rb') as f:
        logging.info(f'reading input dict from {path}')
        dict = pickle.load(f)
        return dict


def read_config_file(path):
    try:
        logging.info(f'reading config from {path}')
        with open(path) as file:
            data = file.read()
        data = dict(json.loads(data))
        logging.info(f'accessing parameters')
        config = data['parameters']

    except Exception as exception:
        config = None
        error_message = f"Read config file - {repr(exception)}"
        logging.info(error_message)
    return config
