#!/usr/bin/python3
"""
Initialize the models package based on the storage type.
"""

from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

# Get the storage type from the environment variable
storage_type = getenv("HBNB_TYPE_STORAGE")

# Initialize the storage based on the storage type
if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

# Load the data from the storage
storage.reload()
