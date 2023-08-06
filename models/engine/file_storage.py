#!/usr/bin/python3
"""Module containing FileStorage class definition.
"""

import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Represents a storage engine structured as key/value pairs.

    Attributes:
    __file_path (str): name of the file used in saving objects to dicts.
    __objects (dict): dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """FileStorage instance initialization."""
        self.reload()

    def all(self, cls=None):
        """Returns a dictionary of instantiated objects in __objects.

        If a cls is specified, a dictionary of objects of that type
        is returned. Otherwise, returns the __objects dictionary.
        """
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            return {
                key: value for key, value in self.__objects.items()
                if isinstance(value, cls)}

        return self.__objects

    def new(self, obj):
        """Set in __objects obj a key <obj_class_name>.id."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file's __file_path."""
        objects_dict = {
            key: value.to_dict() for key,
            value in self.__objects.items()
        }
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(objects_dict, file)

    def reload(self):
        """Deserializes the JSON file's __file_path to __objects,
        if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for obj_data in data.values():
                    class_name = obj_data["__class__"]
                    del obj_data["__class__"]
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes a given instance from __objects, if it exists."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects.pop(key, None)

    def close(self):
        """Call reload method for deserializing the JSON file to objects."""
        self.reload()

    def get(self, cls, id):
        """Retrieve an object based on class and ID"""
        key = "{}.{}".format(cls.__name__, id)
        return self.all(cls).get(key, None)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            return len([obj for obj in self.all(
                cls).values() if isinstance(obj, cls)])
        return len(self.all())
