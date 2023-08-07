#!/usr/bin/python3
"""
Contains test cases for the FileStorage class and its documentation.
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of the FileStorage class.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up for the documentation tests.
        """
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """
        Ensure models/engine/file_storage.py conforms to PEP8 code style.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """
        Ensure tests/test_models/test_file_storage.py conforms to PEP8 code style.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """
        Ensure file_storage.py module has a docstring.
        """
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """
        Ensure FileStorage class has a docstring.
        """
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """
        Ensure FileStorage methods have docstrings.
        """
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """
    Test cases for the FileStorage class.
    """
    @unittest.skipIf(models.storage_type == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """
        Test that the 'all' method returns the FileStorage.__objects attribute.
        """
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_type == 'db', "not testing file storage")
    def test_new(self):
        """
        Test that the 'new' method adds an object to the FileStorage.__objects attribute.
        """
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    @unittest.skipIf(models.storage_type == 'db', "not testing file storage")
    def test_save(self):
        """
        Test that the 'save' method properly saves objects to file.json.
        """
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])
        storage.save()
        with open("file.json", "r") as f:
            data = json.load(f)
        self.assertIn(key, data)

    @unittest.skipIf(models.storage_type == 'db', "not testing file storage")
    def test_get(self):
        """
        Test that the 'get' method returns an object with a given id.
        """
        storage = FileStorage()

        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                storage.new(instance)
                obj = storage.get(value, instance.id)
                not_exists = storage.get(value, None)
                self.assertEqual(instance, obj)
                self.assertEqual(not_exists, None)

    @unittest.skipIf(models.storage_type == 'db', "not testing file storage")
    def test_count(self):
        """
        Test that the 'count' method returns the number of objects in storage.
        """
        storage = FileStorage()

        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                storage.new(instance)
                count = storage.count(value)
                self.assertGreaterEqual(count, 1)
        total = storage.count()
        self.assertGreaterEqual(total, 1)
