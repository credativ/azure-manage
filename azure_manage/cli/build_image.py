# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os
import subprocess
import sys
import yaml

from . import CliBase, setup_argparse
from ..vhd import VHDFooter


class Cli(CliBase):
    parser = setup_argparse(description='Build image')
    parser.add_argument('--bindir', metavar='BINDIR', default=os.path.dirname(os.path.realpath(sys.argv[0])))

    def __init__(self):
        super().__init__()

        self.release = self.config_get('release')
        self.image_prefix = self.config_get('image_prefix')
        self.image_size_gb = self.config_get('image_size_gb')

    def __call__(self):
        workdir = self.workdir

        filename_image = os.path.join(workdir, '{}.vhd'.format(self.config_get('image_prefix')))
        filename_meta = os.path.join(workdir, '{}.yaml'.format(self.config_get('image_prefix')))

        os.umask(0o22)
        if not os.path.isdir(workdir):
            os.makedirs(workdir)

        with open(filename_image, 'wb') as f:
            pass

        subprocess.check_call(
            (
                'sudo',
                os.path.join(self.args.bindir, 'azure_build_image_debian'),
                '--release', self.release,
                '--output', filename_image,
                '--debootstrap-url', 'http://debian-archive.trafficmanager.net/debian',
                '--image-size', str(self.image_size_gb),
            ),
        )

        with open(filename_image, 'rb+') as f:
            f.seek(0, 2)
            image_size = f.tell()
            image_size_complete = image_size + VHDFooter.size
            footer = VHDFooter(image_size)
            f.write(footer.pack())

        with open(filename_meta, 'w') as f:
            yaml.safe_dump({
                'image_prefix': self.image_prefix,
                'image_size': image_size_complete,
            }, f)


def main():
    Cli()()


if __name__ == '__main__':
    main()
