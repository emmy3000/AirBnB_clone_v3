#!/usr/bin/python3
"""
Unit tests for BaseModel class
"""

import unittest
import os
from os import getenv
from models.base_model import BaseModel
import pep8


class TestBaseModelDocs(unittest.TestCase):
    """
    Test the documentation and style of the BaseModel class.
    """

    def test_base_model_docstring(self):
        """
        Test if BaseModel class has a docstring.
        """
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_init_docstring(self):
        """
        Test if the __init__ method of BaseModel has a docstring.
        """
        self.assertIsNot(BaseModel.__init__.__doc__, None,
                         "BaseModel.__init__ method needs a docstring")
        self.assertTrue(len(BaseModel.__init__.__doc__) >= 1,
                        "BaseModel.__init__ method needs a docstring")

    def test_str_docstring(self):
        """
        Test if the __str__ method of BaseModel has a docstring.
        """
        self.assertIsNot(BaseModel.__str__.__doc__, None,
                         "BaseModel.__str__ method needs a docstring")
        self.assertTrue(len(BaseModel.__str__.__doc__) >= 1,
                        "BaseModel.__str__ method needs a docstring")

    def test_save_docstring(self):
        """
        Test if the save method of BaseModel has a docstring.
        """
        self.assertIsNot(BaseModel.save.__doc__, None,
                         "BaseModel.save method needs a docstring")
        self.assertTrue(len(BaseModel.save.__doc__) >= 1,
                        "BaseModel.save method needs a docstring")

    def test_to_dict_docstring(self):
        """
        Test if the to_dict method of BaseModel has a docstring.
        """
        self.assertIsNot(BaseModel.to_dict.__doc__, None,
                         "BaseModel.to_dict method needs a docstring")
        self.assertTrue(len(BaseModel.to_dict.__doc__) >= 1,
                        "BaseModel.to_dict method needs a docstring")


class TestBaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class.
        """
        cls.base = BaseModel()
        cls.base.name = "Kev"
        cls.base.num = 20

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class.
        """
        del cls.base

    def tearDown(self):
        """
        Tear down the test cases.
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_BaseModel(self):
        """
        Test for PEP 8 compliance of the BaseModel module.
        """
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    def test_method_BaseModel(self):
        """
        Test if BaseModel class has the required methods.
        """
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))

    def test_init_BaseModel(self):
        """
        Test if BaseModel instance is of type BaseModel.
        """
        self.assertTrue(isinstance(self.base, BaseModel))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") ==
                     'db', 'Skip for DB storage')
    def test_save_BaseModel(self):
        """
        Test if the save method works.
        """
        self.base.save()
        self.assertNotEqual(self.base.created_at, self.base.updated_at)

    def test_to_dict_BaseModel(self):
        """
        Test if the to_dict method works.
        """
        base_dict = self.base.to_dict()
        self.assertEqual(self.base.__class__.__name__, 'BaseModel')
        self.assertIsInstance(base_dict['created_at'], str)
        self.assertIsInstance(base_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
