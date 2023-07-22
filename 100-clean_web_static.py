#!/usr/bin/python3
"""
Script name: 100-clean_web_static.py

This script creates and distributes an archive to your web servers
using the functions do_pack() and do_deploy().
"""

import os
from fabric.api import env, run, local, put
from datetime import datetime
from fabric.context_managers import lcd

# IP addresses for the web servers assigned to an env variable
env.hosts = ['54.209.192.188', '54.89.30.164']


def do_pack():
    """Create a compressed archive of the web_static folder."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        file = os.path.basename(archive_path)
        name = os.path.splitext(file)[0]

        with settings(warn_only=True):
            if put(archive_path, "/tmp/{}".format(file)).failed:
                return False

            if run("mkdir -p /data/web_static/releases/{}/"
                   .format(name)).failed:
                return False

            if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                   .format(file, name)).failed:
                return False

            if run("mv /data/web_static/releases/{}/web_static/* "
                   "/data/web_static/releases/{}/"
                   .format(name, name)).failed:
                return False

            if run("rm /tmp/{}".format(file)).failed:
                return False

            if run("rm -rf /data/web_static/releases/{}/web_static"
                   .format(name)).failed:
                return False

            if run("rm -rf /data/web_static/current").failed:
                return False

            if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                   .format(name)).failed:
                return False

        return True
    except Exception:
        return False


def deploy():
    """Create and distribute the archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)


def do_clean(number=0):
    """Delete out-of-date archives."""
    number = int(number)
    if number < 0:
        return
    elif number == 0:
        number = 1

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -d '\n' rm -f".format(number + 1))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs -d '\n' rm -rf".format(number + 1))
