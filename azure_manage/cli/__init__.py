# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import argparse

from ..config import Config


class ArgsActionDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        namespace_values = getattr(namespace, self.dest, None) or {}

        key, value = values.split('=', 1)
        namespace_values[key] = value

        setattr(namespace, self.dest, namespace_values)


def setup_argparse(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--config', metavar='CONFIG', default=None)
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

        if self.args.config:
            with open(self.args.config) as c:
                self.config_section = Config(c)[self.args.section]
        else:
            self.config_section = {}

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

    def config_get_expand(self, key, default=__marker):
        config = self.config_section
        if default is self.__marker:
            value = config[key]
        else:
            value = config.get(key, default)
        return self.__config_expand(value)

    @property
    def workdir(self):
        return self.args.workdir
