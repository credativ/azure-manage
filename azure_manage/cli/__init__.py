# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import argparse

from ..config import Config


def setup_argparse(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--auto', action='store_true')
    parser.add_argument('--config', metavar='CONFIG', default=None)
    parser.add_argument('--workdir', metavar='WORKDIR', help='working directory (default: ./SECTION-VERSION)')
    parser.add_argument('section', metavar='SECTION')
    parser.add_argument('version', metavar='VERSION')
    return parser


class CliBase:
    def __init__(self):
        self.args = self.parser.parse_args()

        with open(self.args.config) as c:
            self.config_section = Config(c)[self.args.section]

    @property
    def workdir(self):
        return self.args.workdir or './{section}-{version}'.format_map(vars(self.args))
