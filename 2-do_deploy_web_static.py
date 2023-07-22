#!/usr/bin/python3
"""
Script name: `2-do_deploy_web_static.py`

This script distributes an archive to your web servers,
using the function do_deploy.
"""

import os.path
from fabric.api import env, put, run
from contextlib import contextmanager

env.hosts = ["54.209.192.188", "54.89.30.164"]


@contextmanager
def clean_remote_directory(path):
    try:
        yield
    finally:
        run("rm -rf {}".format(path))


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.

    Arguments:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations have been done correctly,
        False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    file = os.path.basename(archive_path)
    name = os.path.splitext(file)[0]

    with clean_remote_directory("/tmp/{}".format(file)), \
            clean_remote_directory("/data/web_static/releases/{}/"
                                   .format(name)):
        if put(archive_path, "/tmp/{}".format(file)).failed:
            return False

        if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
               .format(file, name)).failed:
            return False

        if run("mv /data/web_static/releases/{}/web_static/* "
               "/data/web_static/releases/{}/".format(name, name)).failed:
            return False

    if run("rm /tmp/{}".format(file)).failed or \
       run("rm -rf /data/web_static/releases/{}/web_static"
           .format(name)).failed or \
       run("rm -rf /data/web_static/current").failed or \
       run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
           .format(name)).failed:
        return False

    return True
