#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name='azure-manage',
    version='0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'azure_build_image = azure_manage.cli.build_image:main',
            'azure_upload_image = azure_manage.cli.upload_image:main',
        ]
    },
    scripts=[
        'azure_build_image_debian',
        'azure_extract_publishsettings',
    ],
    install_requires=[
        'azure-servicemanagement-legacy',
        'azure-storage',
        'pyyaml',
    ],
)
