# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import appdirs
import argparse
import logging
import os
import sys

from ..config import Config
from ..servicemanagementservice import ServiceManagementService


logger = logging.getLogger(__name__)


class ArgsActionDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        namespace_values = getattr(namespace, self.dest, None) or {}

        key, value = values.split('=', 1)
        namespace_values[key] = value

        setattr(namespace, self.dest, namespace_values)


def setup_argparse(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--config', metavar='CONFIG', default='config.yml')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--option', metavar='OPTION=VALUE', dest='options',
            default={}, action=ArgsActionDict)
    parser.add_argument('--workdir', metavar='WORKDIR', default='.',
            help='working directory (default: .')
    parser.add_argument('section', metavar='SECTION')
    return parser


class CliBase:
    __marker = object()

    parser = setup_argparse(description='Base')

    def __init__(self, args=None):
        self.args = self.parser.parse_args(args)

        logging.basicConfig(level=self.args.debug and logging.DEBUG or logging.INFO)

        for configdir in ('.', appdirs.user_config_dir('azure-manage')):
            configfile = os.path.join(configdir, self.args.config)
            if os.path.exists(configfile):
                logging.debug('Read config file %s', configfile)
                with open(configfile) as c:
                    self.config_section = Config(c)[self.args.section]
                    self.config_filename_base = os.path.dirname(os.path.realpath(configfile))
                break
        else:
            logging.critical('No config file loaded')
            sys.exit(1)

        for key, value in os.environ.items():
            if key.startswith('AZURE_MANAGE_'):
                key = key[13:].lower()
                self.config_section[key] = value

        self.config_section.update(self.args.options)

    def __config_expand(self, item):
        if isinstance(item, str):
            return item.format_map(self.config_section)
        elif isinstance(item, list):
            return [self.__config_expand(v) for v in item]
        elif isinstance(item, dict):
            return {k: self.__config_expand(v) for k, v in item.items()}
        else:
            return item

    def config_get(self, key, default=__marker):
        config = self.config_section
        if default is self.__marker:
            value = config[key]
        else:
            value = config.get(key, default)
        return self.__config_expand(value)

    def config_get_filename(self, key, default=__marker):
        return os.path.join(self.config_filename_base, self.config_get(key, default))

    @property
    def host_base(self):
        return self.config_get('host_base', 'core.windows.net')

    def servicemanager_create(self, cls=ServiceManagementService):
        subscription = self.config_get('subscription')
        subscription_keyfile = self.config_get_filename('subscription_keyfile')
        host = 'management.' + self.host_base
        return cls(subscription, subscription_keyfile, host=host)

    @property
    def workdir(self):
        return self.args.workdir
