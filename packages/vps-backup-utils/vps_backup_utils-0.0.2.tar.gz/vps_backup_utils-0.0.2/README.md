# vps_backup_utils

<!-- [![Tests Status](https://github.com/python-poetry/poetry/workflows/Tests/badge.svg?branch=master&event=push)](https://github.com/python-poetry/poetry/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush) -->
![Python 3](https://img.shields.io/badge/Python-3-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/vps_backup_utils?label=PyPI)](https://pypi.org/project/vps_backup_utils/)
[![downloads](https://img.shields.io/pypi/dm/vps_backup_utils)](https://pypistats.org/packages/vps_backup_utils)

Backup Utilities for Linux VPS with MySQL and other data. 

With this package, you can write Python scripts to call cli tools. (need to install cli tools in advance)

## Supported cli

* [x] `mysqldump`
* [ ] `pg_dump`
* [x] `tar`
* [x] `gzip`
* [x] `rsync` (to remote servers)

## Usage

1. Run `pip install vps_backup_utils` on your VPS
2. Write a Python script like the below one, and save on your VPS
3. Add this script to your VPS's crontab

```python
#!/usr/bin/env python

from vps_backup_utils import VPSBackupUtils

backuper = VPSBackupUtils('~/backup')
backuper.remove_old_backups(30)
backuper.mysqldump_backup(
    backup_prefix='project1',
    host='127.0.0.1',
    port='3306',
    user='root',
    password='password',
    databases=None,
    gzipped=True
)
backuper.tar_backup(
    backup_prefix='project1',
    src_folder='/path/to/project1/data'
)
backuper.mysqldump_backup(
    backup_prefix='another_project',
    host='127.0.0.1',
    port='3307',
    user='root',
    password='password',
    databases=None,
    gzipped=True
)
backuper.rsync_backups_to_remote(
    host='another.server',
    user='user',
    remote_backup_path='~/server1-backup',
    port='22222',
    delete_mode=True
)
```

## develop

### install dependencies

```
pip3 install poetry
poetry install
```

### test on host machine

Write your codes to `main.py`, and just run.

```
python3 main.py
```

### run unit tests on host machine (not recommended)

```
poetry run pytest
```

### run unit tests on docker (recommended)

```
docker-compose up -d mysql postgresql
docker-compose up pytest --build
```

### build & publish

```
poetry install
poetry build
poetry publish
```
