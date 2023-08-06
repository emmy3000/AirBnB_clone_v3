#!/usr/bin/python3
"""
Unit tests for City class
"""

import unittest
import os
from models.city import City
from models.base_model import BaseModel
import pep8


class TestCity(unittest.TestCase):
    """
    Test cases for the City class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class.
        """
        cls.city = City()
        cls.city.name = "LA"
        cls.city.state_id = "CA"

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class.
        """
        del cls.city

    def tearDown(self):
        """
        Tear down the test cases.
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_City(self):
        """
        Test for PEP 8 compliance of the City module.
        """
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    def test_checking_for_docstring_City(self):
        """
        Test if City class has a docstring.
        """
        self.assertIsNotNone(City.__doc__)

    def test_attributes_City(self):
        """
        Test if City instance has the required attributes.
        """
        self.assertTrue('id' in self.city.__dict__)
        self.assertTrue('created_at' in self.city.__dict__)
        self.assertTrue('updated_at' in self.city.__dict__)
        self.assertTrue('state_id' in self.city.__dict__)
        self.assertTrue('name' in self.city.__dict__)

    def test_is_subclass_City(self):
        """
        Test if City is a subclass of BaseModel.
        """
        self.assertTrue(issubclass(City, BaseModel))

    def test_attribute_types_City(self):
        """
        Test the attribute types of City instance.
        """
        self.assertEqual(type(self.city.name), str)
        self.assertEqual(type(self.city.state_id), str)

    def test_save_City(self):
        """
        Test if the save method works.
        """
        self.city.save()
        self.assertNotEqual(self.city.created_at, self.city.updated_at)

    def test_to_dict_City(self):
        """
        Test if the to_dict method works.
        """
        city_dict = self.city.to_dict()
        self.assertEqual(self.city.__class__.__name__, 'City')
        self.assertIsInstance(city_dict['created_at'], str)
        self.assertIsInstance(city_dict['updated_at'], str)

    def test_inheritance_from_BaseModel(self):
        """
        Test if City inherits from BaseModel.
        """
        self.assertTrue(issubclass(City, BaseModel))

    def test_name_attribute_default_value(self):
        """
        Test if City's name attribute is an empty string by default.
        """
        city = City()
        self.assertEqual(city.name, "")

    def test_state_id_attribute_default_value(self):
        """
        Test if City's state_id attribute is an empty string by default.
        """
        city = City()
        self.assertEqual(city.state_id, "")

    def test_str_representation(self):
        """
        Test the string representation of City object.
        """
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))


if __name__ == "__main__":
    unittest.main()
