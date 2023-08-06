#!/usr/bin/python3
"""
Unit tests for State class
"""

import unittest
import os
from models.state import State
from models.base_model import BaseModel
import pep8


class TestState(unittest.TestCase):
    """
    Test cases for the State class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class
        """
        cls.state = State()
        cls.state.name = "CA"

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class
        """
        del cls.state

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
        Test for PEP 8 compliance of the State module
        """
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    def test_docstring(self):
        """
        Test if State class has a docstring
        """
        self.assertIsNotNone(State.__doc__)

    def test_class_attributes(self):
        """
        Test if State instance has the required attributes
        """
        self.assertTrue('id' in self.state.__dict__)
        self.assertTrue('created_at' in self.state.__dict__)
        self.assertTrue('updated_at' in self.state.__dict__)
        self.assertTrue('name' in self.state.__dict__)

    def test_is_subclass(self):
        """
        Test if State is a subclass of BaseModel
        """
        self.assertTrue(issubclass(self.state.__class__, BaseModel), True)

    def test_attribute_types(self):
        """
        Test the attribute types of State instance
        """
        self.assertEqual(type(self.state.name), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE")
                     == 'db', 'Skip for DB storage')
    def test_save(self):
        """
        Test if the save method works
        """
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict(self):
        """
        Test if the to_dict method works
        """
        state_dict = self.state.to_dict()
        self.assertEqual(self.state.__class__.__name__, 'State')
        self.assertIsInstance(state_dict['created_at'], str)
        self.assertIsInstance(state_dict['updated_at'], str)

    def test_inheritance_from_BaseModel(self):
        """
        Test if State inherits from BaseModel
        """
        self.assertTrue(issubclass(State, BaseModel))

    def test_default_name_value(self):
        """
        Test if State has the default attribute value for name
        """
        state = State()
        self.assertEqual(state.name, "")

    def test_str_representation(self):
        """
        Test the string representation of State object
        """
        string = "[State] ({}) {}".format(self.state.id, self.state.__dict__)
        self.assertEqual(string, str(self.state))

    def test_method_docstrings(self):
        """
        Test for the presence and quality of docstrings in State methods
        """
        for name, method in inspect.getmembers(
                State, predicate=inspect.isfunction):
            self.assertIsNotNone(
                method.__doc__,
                "{} method needs a docstring".format(
                    self.name))
            self.assertTrue(len(method.__doc__) >= 1,
                            "{} method needs a docstring".format(self.name))


if __name__ == "__main__":
    unittest.main()
