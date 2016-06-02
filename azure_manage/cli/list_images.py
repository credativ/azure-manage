# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import argparse
import os
from pprint import pprint

from . import CliBase, setup_argparse


class Cli(CliBase):
    parser = setup_argparse(description='List images')
    parser.add_argument('--category', metavar='CATEGORY', default=None,
            help='filter on category')

    def __init__(self):
        super().__init__()

        self.image_family = self.config_get('image_family', None)

        self.servicemanager = self.servicemanager_create()

    def __call__(self):
        for i in self.servicemanager.list_os_images():
            if self.image_family and i.image_family != self.image_family:
                continue
            if self.args.category and i.category != self.args.category:
                continue

            print(i.name)


def main():
    Cli()()


if __name__ == '__main__':
    main()
