#!/usr/bin/python3
"""
Unit tests for Amenity class
"""

import unittest
import os
from models.amenity import Amenity
from models.base_model import BaseModel
import pep8
import json


class TestAmenityDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of the Amenity class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up for the doc tests.
        """
        cls.amenity_f = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conformance_amenity(self):
        """
        Test that models/amenity.py conforms to PEP8.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenity_module_docstring(self):
        """
        Test for the amenity.py module docstring.
        """
        self.assertIsNot(Amenity.__doc__, None,
                         "amenity.py needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_amenity_class_docstring(self):
        """
        Test for the Amenity class docstring.
        """
        self.assertIsNot(Amenity.__doc__, None,
                         "Amenity class needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_amenity_func_docstrings(self):
        """
        Test for the presence of docstrings in Amenity methods.
        """
        for func in self.amenity_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestAmenity(unittest.TestCase):
    """
    Test cases for the Amenity class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class.
        """
        cls.amenity = Amenity()
        cls.amenity.name = "Breakfast"

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class.
        """
        del cls.amenity

    def tearDown(self):
        """
        Tear down the test cases.
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Amenity(self):
        """
        Test for PEP 8 compliance of the Amenity module.
        """
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    def test_checking_for_docstring_Amenity(self):
        """
        Test if Amenity class has a docstring.
        """
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes_Amenity(self):
        """
        Test if Amenity instance has all the required attributes.
        """
        self.assertTrue('id' in self.amenity.__dict__)
        self.assertTrue('created_at' in self.amenity.__dict__)
        self.assertTrue('updated_at' in self.amenity.__dict__)
        self.assertTrue('name' in self.amenity.__dict__)

    def test_is_subclass_Amenity(self):
        """
        Test if Amenity is a subclass of BaseModel.
        """
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_attribute_types_Amenity(self):
        """
        Test the attribute types of Amenity.
        """
        self.assertEqual(type(self.amenity.name), str)

    def test_save_Amenity(self):
        """
        Test if the save method works.
        """
        self.amenity.save()
        self.assertNotEqual(self.amenity.created_at, self.amenity.updated_at)

    def test_to_dict_Amenity(self):
        """
        Test if the to_dict method works.
        """
        self.assertTrue('to_dict' in dir(self.amenity))


if __name__ == "__main__":
    unittest.main()
