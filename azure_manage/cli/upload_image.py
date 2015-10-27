# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os

from ..blobservice import BlobService
from ..config import Config
from ..progress import ProgressOutput
from ..servicemanagementservice import ServiceManagementService
from . import CliBase, setup_argparse


class Cli(CliBase):
    parser = setup_argparse(description='Upload image')

    def __init__(self):
        super().__init__()

        self.image_prefix = self.config_get('image_prefix')
        self.image_filename = os.path.join(self.workdir, self.image_prefix + '.raw')
        self.image_name = self.config_get('image_name')
        self.image_label = self.config_get('image_label', self.image_name)
        self.image_meta = self.config_get('image_meta')

        self.storage_account = self.config_get('storage_account')
        self.storage_container = self.config_get('storage_container')
        self.storage_name = self.image_prefix + '.vhd'

        self.subscription = self.config_get('subscription')
        self.subscription_keyfile = self.config_get('subscription_keyfile')

    def __call__(self):
        with ProgressOutput() as progress_stream:
            servicemanager = ServiceManagementService(self.subscription, self.subscription_keyfile)
            self.do_upload(servicemanager, progress_stream)
            self.do_register(servicemanager, progress_stream)

    def do_upload(self, servicemanager, progress_stream):
        print('Looking up storage {}'.format(self.storage_account))
        storage = servicemanager.get_storage_account_keys(self.storage_account)
        storage_key = storage.storage_service_keys.primary

        print('Upload image {}/{}/{}'.format(self.storage_account, self.storage_container, self.storage_name))
        blob = BlobService(self.storage_account, storage_key)
        self.storage_url = blob.put_rawimage_from_path(self.storage_container, self.storage_name, self.image_filename, progress_stream)
        print('Finished upload image {}'.format(self.storage_url))

    def do_register(self, servicemanager, progress_stream):
        print('Register image {} ({})'.format(self.image_name, self.image_label))
        progress_stream.write_progress('Register image')
        servicemanager.add_os_image(self.image_label, self.storage_url, self.image_name, 'Linux', **self.image_meta)
        print('Finished register image')
        progress_stream.write_progress('')


def main():
    Cli()()


if __name__ == '__main__':
    main()
