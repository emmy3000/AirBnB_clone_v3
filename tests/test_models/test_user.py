#!/usr/bin/python3
"""
Unit tests for User class
"""

import unittest
import os
from models.user import User
from models.base_model import BaseModel
import pep8


class TestUser(unittest.TestCase):
    """
    Test cases for the User class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class
        """
        cls.user = User()
        cls.user.first_name = "Kevin"
        cls.user.last_name = "Yook"
        cls.user.email = "yook00627@gmamil.com"
        cls.user.password = "secret"

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class
        """
        del cls.user

    def tearDown(self):
        """
        Tear down the test cases
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8(self):
        """
        Test for PEP 8 compliance of the User module
        """
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    def test_docstring(self):
        """
        Test if User class has a docstring
        """
        self.assertIsNotNone(User.__doc__)

    def test_class_attributes(self):
        """
        Test if User instance has the required attributes
        """
        user = User()
        attributes = [
            "email",
            "id",
            "created_at",
            "updated_at",
            "password",
            "first_name",
            "last_name"]
        for attr in attributes:
            self.assertTrue(hasattr(user, attr))

    def test_is_subclass(self):
        """
        Test if User is a subclass of BaseModel
        """
        user = User()
        self.assertTrue(issubclass(user.__class__, BaseModel))

    def test_attribute_types(self):
        """
        Test the attribute types of User instance
        """
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE")
                     == 'db', 'Skip for DB storage')
    def test_save(self):
        """
        Test if the save method works
        """
        self.user.save()
        with open("file.json", "r") as file:
            content = file.read()
            self.assertIn("User." + self.user.id, content)

    def test_to_dict(self):
        """
        Test if the to_dict method works
        """
        user_dict = self.user.to_dict()
        self.assertEqual(self.user.__class__.__name__, 'User')
        self.assertIsInstance(user_dict['created_at'], str)
        self.assertIsInstance(user_dict['updated_at'], str)

    def test_inheritance_from_BaseModel(self):
        """
        Test if User inherits from BaseModel
        """
        self.assertTrue(issubclass(User, BaseModel))

    def test_default_attribute_values(self):
        """
        Test if User has the default attribute values
        """
        user = User()
        default_values = {
            "email": "",
            "password": "",
            "first_name": "",
            "last_name": ""}
        for attr, value in default_values.items():
            self.assertEqual(getattr(user, attr), value)

    def test_str_representation(self):
        """
        Test the string representation of User object
        """
        string = "[User] ({}) {}".format(self.user.id, self.user.__dict__)
        self.assertEqual(string, str(self.user))

    def test_method_docstrings(self):
        """
        Test for the presence and quality of docstrings in User methods
        """
        for name, method in inspect.getmembers(
                User, predicate=inspect.isfunction):
            self.assertIsNotNone(
                method.__doc__,
                "{} method needs a docstring".format(
                    self.name))
            self.assertTrue(len(method.__doc__) >= 1,
                            "{} method needs a docstring".format(self.name))


if __name__ == "__main__":
    unittest.main()
