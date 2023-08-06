#!/usr/bin/python3
"""
Unit tests for Review class
"""

import unittest
import os
from os import getenv
from models.review import Review
from models.base_model import BaseModel
import pep8


class TestReview(unittest.TestCase):
    """
    Test cases for the Review class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class
        """
        cls.review = Review()
        cls.review.place_id = "4321-dcba"
        cls.review.user_id = "123-bca"
        cls.review.text = "The strongest in the Galaxy"

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class
        """
        del cls.review

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
        Test for PEP 8 compliance of the Review module
        """
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    def test_docstring(self):
        """
        Test if Review class has a docstring
        """
        self.assertIsNotNone(Review.__doc__)

    def test_class_attributes(self):
        """
        Test if Review instance has the required attributes
        """
        self.assertTrue('id' in self.review.__dict__)
        self.assertTrue('created_at' in self.review.__dict__)
        self.assertTrue('updated_at' in self.review.__dict__)
        self.assertTrue('place_id' in self.review.__dict__)
        self.assertTrue('user_id' in self.review.__dict__)
        self.assertTrue('text' in self.review.__dict__)

    def test_is_subclass(self):
        """
        Test if Review is a subclass of BaseModel
        """
        self.assertTrue(issubclass(self.review.__class__, BaseModel), True)

    def test_attribute_types(self):
        """
        Test the attribute types of Review instance
        """
        self.assertEqual(type(self.review.text), str)
        self.assertEqual(type(self.review.place_id), str)
        self.assertEqual(type(self.review.user_id), str)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") ==
                     'db', 'Skip for DB storage')
    def test_save(self):
        """
        Test if the save method works
        """
        self.review.save()
        self.assertNotEqual(self.review.created_at, self.review.updated_at)

    def test_to_dict(self):
        """
        Test if the to_dict method works
        """
        review_dict = self.review.to_dict()
        self.assertEqual(self.review.__class__.__name__, 'Review')
        self.assertIsInstance(review_dict['created_at'], str)
        self.assertIsInstance(review_dict['updated_at'], str)

    def test_inheritance_from_BaseModel(self):
        """
        Test if Review inherits from BaseModel
        """
        self.assertTrue(issubclass(Review, BaseModel))

    def test_default_attribute_values(self):
        """
        Test if Review has default attribute values as expected
        """
        # Add test cases to check default attribute values
        self.assertEqual(self.review.place_id, "4321-dcba")
        self.assertEqual(self.review.user_id, "123-bca")
        self.assertEqual(self.review.text, "The strongest in the Galaxy")

    def test_str_representation(self):
        """
        Test the string representation of Review object
        """
        string = "[Review] ({}) {}".format(
            self.review.id, self.review.__dict__)
        self.assertEqual(string, str(self.review))

    def test_method_docstrings(self):
        """
        Test for the presence and quality of docstrings in Review methods
        """
        for name, method in inspect.getmembers(
                Review, predicate=inspect.isfunction):
            self.assertIsNotNone(
                method.__doc__,
                f"{name} method needs a docstring")
            self.assertTrue(len(method.__doc__) >= 1,
                            f"{name} method needs a docstring")


if __name__ == "__main__":
    unittest.main()
