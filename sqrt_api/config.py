"""Модул конфига"""
import logging
import os
import sys

import yaml

LOGGER = logging.getLogger(__name__)


class Config(dict):
    """
    Класс dict типа с конфигурационными данными
    """
    def __init__(self, *args, **kwargs):
        path = os.getenv('CONFIG', "./config.yaml")
        conf = {}
        try:
            with open(path) as file:
                yaml_conf = yaml.load(file, Loader=yaml.FullLoader)
                conf.update(yaml_conf)
        except EnvironmentError as error:
            LOGGER.error('Cant load config file. exiting...[%s]', error)
            sys.exit(-1)
        except yaml.YAMLError as error:
            LOGGER.error('Config file is broken. [%s]', error)
            LOGGER.info('Exiting ...')
            sys.exit(-1)

        super().__init__(conf, *args, **kwargs)

        LOGGER.info('Config %s loaded.', path)

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)

    def __iter__(self):
        return dict.__iter__(self)

    def __len__(self):
        return dict.__len__(self)


CONFIG = Config()
