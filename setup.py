#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name='azure-manage',
    version='0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'build_image = azure_manage.cli.build_image:main',
            'upload_image = azure_manage.cli.upload_image:main',
        ]
    },
    scripts=[
        'build_image_debian_azure',
        'extract_publishsettings',
    ],
)
