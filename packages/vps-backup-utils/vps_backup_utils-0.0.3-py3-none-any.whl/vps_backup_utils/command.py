"""
This module convert Python functions to shell commands.
"""

import logging
import os
from .utils.paths import Path, quote_path
from typing import List, Union

logger = logging.getLogger(__name__)


def run_command(cmd: str):
    logger.info(f"Executing: {cmd}")
    if os.system(cmd) != 0:
        raise Exception(f"Command {cmd} failed")


def gzip(target: Path):
    gzip_cmd = f"gzip -f {quote_path(target)}"
    run_command(gzip_cmd)


def tar(target: Path,
        src: Path,
        gzipped=True):
    """
    tar folder
    """
    os.chdir(src)
    tar_cmd = f"tar {'-czf' if gzipped else '-cf'} {quote_path(target)} ."
    run_command(tar_cmd)


def rsync(local_path: Path,
          host: str,
          user: str,
          remote_path: Path,
          port: str,
          is_upload=True,
          delete_mode=True):
    """
    sync backup folder to remote server
    need `rsync` in PATH, and ssh key configured
    """
    _local_path = quote_path(local_path)
    _remote_path = f"{user}@{host}:{quote_path(remote_path)}"
    if is_upload:
        paths = f"{_local_path} {_remote_path}"
    else:
        paths = f"{_remote_path} {_local_path}"
    rsync_cmd = f"""rsync \\
        --archive \\
        --verbose \\
        --human-readable \\
        {'--delete' if delete_mode else ''} \\
        -e "ssh -p {port}" \\
        {paths}"""
    run_command(rsync_cmd)


def mysqldump(host: str,
              port: str,
              user: str,
              password: str,
              db: str,
              all_databases: bool,
              output_filename: Path):
    _db = '--all-databases' if all_databases else db
    dump_cmd = f"""mysqldump \\
        -h {host} \\
        -P {port} \\
        -u {user} \\
        -p{password} \\
        {_db} \\
        > {quote_path(output_filename)}"""
    run_command(dump_cmd)


def pg_dump(host: str,
            port: str,
            db: str,
            all_databases: bool,
            output_filename: Path):
    _cli = "pg_dumpall" if all_databases else f"pg_dump {db}"
    dump_cmd = f"""{_cli} \\
        -h {host} \\
        -p {port} \\
        {db} \\
        > {quote_path(output_filename)}"""
    run_command(dump_cmd)
