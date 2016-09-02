#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name='azure-manage',
    version='0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'azure_build_image = azure_manage.cli.build_image:main',
            'azure_delete_image = azure_manage.cli.delete_image:main',
            'azure_list_images = azure_manage.cli.list_images:main',
            'azure_upload_image = azure_manage.cli.upload_image:main',
        ]
    },
    scripts=[
        'azure_build_image_debian',
        'azure_extract_publishsettings',
    ],
    install_requires=[
        'appdirs',
        'azure-servicemanagement-legacy',
        'azure-storage>=0.33',
        'pyyaml',
    ],
)
