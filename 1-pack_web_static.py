#!/usr/bin/python3
"""
Script name: `1-pack_web_static.py`
This script creates a compressed archive of the web_static folder.
"""

import os
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a compressed archive of the web_static folder.

    Returns:
        str: Path of the generated archive if successful, None otherwise.
    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + current_time + ".tgz"
    archive_path = "versions/" + archive_name

    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None
