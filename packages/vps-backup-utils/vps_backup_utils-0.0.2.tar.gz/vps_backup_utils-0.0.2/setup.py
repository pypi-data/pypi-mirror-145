# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vps_backup_utils', 'vps_backup_utils.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vps-backup-utils',
    'version': '0.0.2',
    'description': 'Backup Utilities for Linux VPS with MySQL and other data',
    'long_description': "# vps_backup_utils\n\n<!-- [![Tests Status](https://github.com/python-poetry/poetry/workflows/Tests/badge.svg?branch=master&event=push)](https://github.com/python-poetry/poetry/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush) -->\n![Python 3](https://img.shields.io/badge/Python-3-blue.svg)\n[![PyPI](https://img.shields.io/pypi/v/vps_backup_utils?label=PyPI)](https://pypi.org/project/vps_backup_utils/)\n[![downloads](https://img.shields.io/pypi/dm/vps_backup_utils)](https://pypistats.org/packages/vps_backup_utils)\n\nBackup Utilities for Linux VPS with MySQL and other data. \n\nWith this package, you can write Python scripts to call cli tools. (need to install cli tools in advance)\n\n## Supported cli\n\n* [x] `mysqldump`\n* [ ] `pg_dump`\n* [x] `tar`\n* [x] `gzip`\n* [x] `rsync` (to remote servers)\n\n## Usage\n\n1. Run `pip install vps_backup_utils` on your VPS\n2. Write a Python script like the below one, and save on your VPS\n3. Add this script to your VPS's crontab\n\n```python\n#!/usr/bin/env python\n\nfrom vps_backup_utils import VPSBackupUtils\n\nbackuper = VPSBackupUtils('~/backup')\nbackuper.remove_old_backups(30)\nbackuper.mysqldump_backup(\n    backup_prefix='project1',\n    host='127.0.0.1',\n    port='3306',\n    user='root',\n    password='password',\n    databases=None,\n    gzipped=True\n)\nbackuper.tar_backup(\n    backup_prefix='project1',\n    src_folder='/path/to/project1/data'\n)\nbackuper.mysqldump_backup(\n    backup_prefix='another_project',\n    host='127.0.0.1',\n    port='3307',\n    user='root',\n    password='password',\n    databases=None,\n    gzipped=True\n)\nbackuper.rsync_backups_to_remote(\n    host='another.server',\n    user='user',\n    remote_backup_path='~/server1-backup',\n    port='22222',\n    delete_mode=True\n)\n```\n\n## develop\n\n### install dependencies\n\n```\npip3 install poetry\npoetry install\n```\n\n### test on host machine\n\nWrite your codes to `main.py`, and just run.\n\n```\npython3 main.py\n```\n\n### run unit tests on host machine (not recommended)\n\n```\npoetry run pytest\n```\n\n### run unit tests on docker (recommended)\n\n```\ndocker-compose up -d mysql postgresql\ndocker-compose up pytest --build\n```\n\n### build & publish\n\n```\npoetry install\npoetry build\npoetry publish\n```\n",
    'author': 'lyh543',
    'author_email': 'lyh543@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lyh543/vps_backup_utils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
