#!/usr/bin/python3
"""
Unit tests for Place class
"""

import unittest
import os
from os import getenv
from models.place import Place
from models.base_model import BaseModel
import pep8


class TestPlace(unittest.TestCase):
    """
    Test cases for the Place class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class
        """
        cls.place = Place()
        cls.place.city_id = "1234-abcd"
        cls.place.user_id = "4321-dcba"
        cls.place.name = "Death Star"
        cls.place.description = "UNLIMITED POWER!!!!!"
        cls.place.number_rooms = 1000000
        cls.place.number_bathrooms = 1
        cls.place.max_guest = 607360
        cls.place.price_by_night = 10
        cls.place.latitude = 160.0
        cls.place.longitude = 120.0
        cls.place.amenity_ids = ["1324-lksdjkl"]

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class
        """
        del cls.place

    def tearDown(self):
        """
        Tear down the test
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Place(self):
        """
        Test for PEP 8 compliance of the Place module
        """
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    def test_checking_for_docstring_Place(self):
        """
        Test if Place class has a docstring
        """
        self.assertIsNotNone(Place.__doc__)

    def test_class_docstring_Place(self):
        """
        Test if Place class docstring is well-defined
        """
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class needs a docstring")

    def test_attributes_Place(self):
        """
        Test if Place instance has the required attributes
        """
        self.assertTrue('id' in self.place.__dict__)
        self.assertTrue('created_at' in self.place.__dict__)
        self.assertTrue('updated_at' in self.place.__dict__)
        self.assertTrue('city_id' in self.place.__dict__)
        self.assertTrue('user_id' in self.place.__dict__)
        self.assertTrue('name' in self.place.__dict__)
        self.assertTrue('description' in self.place.__dict__)
        self.assertTrue('number_rooms' in self.place.__dict__)
        self.assertTrue('number_bathrooms' in self.place.__dict__)
        self.assertTrue('max_guest' in self.place.__dict__)
        self.assertTrue('price_by_night' in self.place.__dict__)
        self.assertTrue('latitude' in self.place.__dict__)
        self.assertTrue('longitude' in self.place.__dict__)
        self.assertTrue('amenity_ids' in self.place.__dict__)

    def test_is_subclass_Place(self):
        """
        Test if Place is a subclass of BaseModel
        """
        self.assertTrue(issubclass(self.place.__class__, BaseModel), True)

    def test_attribute_types_Place(self):
        """
        Test the attribute types of Place instance
        """
        self.assertEqual(type(self.place.city_id), str)
        self.assertEqual(type(self.place.user_id), str)
        self.assertEqual(type(self.place.name), str)
        self.assertEqual(type(self.place.description), str)
        self.assertEqual(type(self.place.number_rooms), int)
        self.assertEqual(type(self.place.number_bathrooms), int)
        self.assertEqual(type(self.place.max_guest), int)
        self.assertEqual(type(self.place.price_by_night), int)
        self.assertEqual(type(self.place.latitude), float)
        self.assertEqual(type(self.place.longitude), float)
        self.assertEqual(type(self.place.amenity_ids), list)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") ==
                     'db', 'Skip for DB storage')
    def test_save_Place(self):
        """
        Test if the save method works
        """
        self.place.save()
        self.assertNotEqual(self.place.created_at, self.place.updated_at)

    def test_to_dict_Place(self):
        """
        Test if the to_dict method works
        """
        place_dict = self.place.to_dict()
        self.assertEqual(self.place.__class__.__name__, 'Place')
        self.assertIsInstance(place_dict['created_at'], str)
        self.assertIsInstance(place_dict['updated_at'], str)

    def test_inheritance_from_BaseModel(self):
        """
        Test if Place inherits from BaseModel
        """
        self.assertTrue(issubclass(Place, BaseModel))

    def test_default_attribute_values(self):
        """
        Test if Place has default attribute values as expected
        """
        place = Place()
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.name, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, [])

    def test_str_representation(self):
        """
        Test the string representation of Place object
        """
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))

    def test_method_docstrings(self):
        """
        Test for the presence and quality of docstrings in Place methods
        """
        for name, method in inspect.getmembers(
                Place, predicate=inspect.isfunction):
            self.assertIsNotNone(
                method.__doc__,
                "{} method needs a docstring".format(self.name))
            self.assertTrue(len(method.__doc__) >= 1,
                            "{} method needs a docstring".format(self.name))

    def test_module_docstring(self):
        """
        Test for the place.py module docstring
        """
        self.assertIsNotNone(__doc__, "place.py needs a docstring")
        self.assertTrue(len(__doc__) >= 1, "place.py needs a docstring")


if __name__ == "__main__":
    unittest.main()
