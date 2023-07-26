#!/usr/bin/python3
"""
Script name: 100-clean_web_static.py

This script deletes out-dated archives by
utilizing the do_clean() function.
"""
import os
from fabric.api import env, run, local

# IP addresses for the web servers assigned to an env variable
env.hosts = ['54.209.192.188', '54.89.30.164']


def do_clean(number=0):
    """
    Delete out-dated archives.

    Args:
        number (int): The number of archives retained.

    If number == 0 || 1, retains only the most recent archive.
    If number == 2, retains either most recent || 2nd most recent archives
    """
    number = int(number)
    number = 1 if number < 1 else number

    # Local clean up
    os.chdir("./versions")
    archives = sorted(os.listdir("."))
    archives = archives[:-number]
    [local("rm {}".format(a)) for a in archives]

    # Remote clean up
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        archives = archives[:-number]
        [run("rm -rf {}".format(a)) for a in archives]
