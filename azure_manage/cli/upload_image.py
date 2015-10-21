# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import argparse

from azure_manage.blobservice import BlobService
from azure_manage.config import Config
from azure_manage.progress import ProgressOutput
from azure_manage.servicemanagementservice import ServiceManagementService


class Main:
    parser = argparse.ArgumentParser(description='Upload image')
    parser.add_argument('--auto', action='store_true')
    parser.add_argument('--config', metavar='CONFIG', default=None)
    parser.add_argument('section', metavar='SECTION')
    parser.add_argument('version', metavar='VERSION')

    def __init__(self):
        args = self.parser.parse_args()

        with open(args.config) as c:
            config_section = Config(c)[args.section]

        if args.auto and not config_section.get('image_auto_upload'):
            print('Automatic mode and no automatic upload allowed, ignoring')
            sys.exit(0)

        self.image_name = config_section['image_name'].format_map(vars(args))
        self.image_label = config_section.get('image_label', self.image_name)
        self.image_meta = config_section['image_meta']
        self.image_filename = self.image_name + '.raw'

        self.storage_account = config_section['storage_account']
        self.storage_container = config_section['storage_container']
        self.storage_key = config_section['storage_key']
        self.storage_name = self.image_name + '.vhd'

        self.subscription = config_section['subscription']
        self.subscription_keyfile = config_section['subscription_keyfile']

    def __call__(self):
        with ProgressOutput() as progress_stream:
            self.do_upload(progress_stream)
            self.do_register(progress_stream)

    def do_upload(self, progress_stream):
        print('Upload image {}/{}/{}'.format(self.storage_account, self.storage_container, self.storage_name))
        blob = BlobService(self.storage_account, self.storage_key)
        self.storage_url = blob.put_rawimage_from_path(self.storage_container, self.storage_name, self.image_filename, progress_stream)
        print('Finished upload image {}'.format(self.storage_url))

    def do_register(self, progress_stream):
        print('Register image {} ({})'.format(self.image_name, self.image_label))
        progress_stream.write_progress('Register image')
        servicemanager = ServiceManagementService(self.subscription, self.subscription_keyfile)
        servicemanager.add_os_image(self.image_label, self.storage_url, self.image_name, 'Linux', **self.image_meta)
        print('Finished register image')
        progress_stream.write_progress('')


def main():
    Main()()
