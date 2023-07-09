#!/usr/bin/python3
"""
Script name: `2-do_deploy_web_static.py`
Fabric script for deploying web_static archives to web servers.
"""

import os
from fabric.api import env, put, run


# Define web servers
env.hosts = ['54.209.192.188', '54.89.30.164']
env.user = 'root'
env.key_filename = '/root/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Distributes the web_static archive to the web servers.

    Args:
        archive_path (str): Path of the web_static archive.

    Returns:
        bool: True if all operations are successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on web servers
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/ directory
        # on web servers
        archive_filename = os.path.basename(archive_path)
        archive_name_without_ext = os.path.splitext(archive_filename)[0]
        releases_path = "/data/web_static/releases/"
        run("mkdir -p {}{}".format(releases_path, archive_name_without_ext))
        run("tar -xzf /tmp/{} -C {}{}"
            .format(archive_filename, releases_path, archive_name_without_ext))

        # Delete the archive from /tmp/ directory on web servers
        run("rm /tmp/{}".format(archive_filename))

        # Delete the symbolic link /data/web_static/current on web servers
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on web servers
        run("ln -s {}{} /data/web_static/current"
            .format(releases_path, archive_name_without_ext))

        return True

    except Exception:
        return False
