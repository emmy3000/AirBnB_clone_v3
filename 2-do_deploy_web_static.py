#!/usr/bin/python3
"""
Script name: `2-do_deploy_web_static.py`

This script distributes an archive to your web servers,
using the function do_deploy.
"""
from fabric.api import env
from fabric.api import put
from fabric.api import run
import os.path

env.hosts = ["54.209.192.188", "54.89.30.164"]


def do_deploy(archive_path):
    """
    Distributes archive to web servers.

    Args:
        archive_path (str): The path of archive to be distributed.

    Returns:
        If file doesn't exist at archive_path or error occurs - return False.
        Otherwise return True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
