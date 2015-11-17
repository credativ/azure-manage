# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os
import subprocess
import sys
import yaml

from . import CliBase, setup_argparse


class Cli(CliBase):
    parser = setup_argparse(description='Build image')
    parser.add_argument('--bindir', metavar='BINDIR', default=os.path.dirname(os.path.realpath(sys.argv[0])))

    def __init__(self):
        super().__init__()

        self.release = self.config_get('release')
        self.image_prefix = self.config_get('image_prefix')
        self.image_size_gb = self.config_get('image_size_gb')

    def __call__(self):
        os.umask(0o22)
        workdir = self.workdir
        if not os.path.isdir(workdir):
            os.makedirs(workdir)

        subprocess.check_call(
            (
                'sudo',
                os.path.join(self.args.bindir, 'azure_build_image_debian'),
                '--release', self.release,
                '--output', os.path.join(workdir, '{}.raw'.format(self.image_prefix)),
                '--debootstrap-url', 'http://debian-archive.trafficmanager.net/debian',
                '--image-size', str(self.image_size_gb),
            ),
        )

        with open(os.path.join(workdir, '{}.yaml'.format(self.image_prefix)), 'w') as f:
            yaml.safe_dump({
                'image_prefix': self.image_prefix,
                'image_size_gb': self.image_size_gb,
            }, f)


def main():
    Cli()()


if __name__ == '__main__':
    main()
