# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os

from ..config import Config
from . import CliBase, setup_argparse


class Cli(CliBase):
    parser = setup_argparse(description='Delete image')
    parser.add_argument('--delete-vhd', action='store_true',
            help='delete image file from storage as well')

    def __init__(self):
        super().__init__()

        self.image_name = self.config_get('image_name')

        self.servicemanager = self.servicemanager_create()

    def __call__(self):
        self.servicemanager.delete_os_image(self.image_name, self.args.delete_vhd)


def main():
    Cli()()


if __name__ == '__main__':
    main()
