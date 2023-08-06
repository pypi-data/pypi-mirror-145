# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vps_backup_utils', 'vps_backup_utils.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vps-backup-utils',
    'version': '0.0.1',
    'description': 'Backup Utilities for Linux VPS with MySQL and other data',
    'long_description': None,
    'author': 'lyh543',
    'author_email': 'lyh543@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
