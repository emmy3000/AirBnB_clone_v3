#!/usr/bin/python3
"""
Unit tests for the HBNB console
"""

import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import json
import console
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    """
    Class for testing the HBNB command-line console
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test cases
        """
        cls.console = HBNBCommand()

    def tearDown(self):
        """
        Remove the temporary file (file.json) created during the test
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_update_missing_class_name(self):
        """
        Test the update command with missing class name
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue()
            )

    def test_update_invalid_class_name(self):
        """
        Test the update command with invalid class name
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )

    def test_update_missing_id(self):
        """
        Test the update command with missing instance id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue()
            )

    def test_update_invalid_id(self):
        """
        Test the update command with invalid instance id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue()
            )

    def test_update_missing_attribute_name(self):
        """
        Test the update command with missing attribute name
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User abcd-123")
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue()
            )

    def test_update_missing_value(self):
        """
        Test the update command with missing value
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User abcd-123 name")
            self.assertEqual(
                "** value missing **\n", f.getvalue()
            )

    def test_update_valid_input(self):
        """
        Test the update command with valid input
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User name='Alice'")
            obj_id = f.getvalue().strip()
            self.console.onecmd("update User {} name 'Bob'".format(obj_id))
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User {}".format(obj_id))
            obj_str = f.getvalue().strip()
            self.assertIn("'name': 'Bob'", obj_str)

    def test_count(self):
        """
        Test the count command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='California'")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State name='New York'")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count State")
            self.assertEqual("2\n", f.getvalue())

    def test_EOF(self):
        """
        Test the EOF signal
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))

    def test_pep8_conformance_console(self):
        """
        Test that console.py conforms to PEP8
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(
            result.total_errors,
            0,
            "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """
        Test that tests/test_console.py conforms to PEP8
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(
            result.total_errors,
            0,
            "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """
        Test for the console.py module docstring
        """
        self.assertIsNot(console.__doc__, None, "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """
        Test for the HBNBCommand class docstring
        """
        self.assertIsNot(
            HBNBCommand.__doc__,
            None,
            "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_testConsole_class_docstring(self):
        """
        Test for the TestConsole class docstring
        """
        self.assertIsNot(
            TestConsole.__doc__,
            None,
            "TestConsole class needs a docstring")
        self.assertTrue(len(TestConsole.__doc__) >= 1,
                        "TestConsole class needs a docstring")

    def test_update_missing_class_name_docstring(self):
        """
        Test docstring for the update_missing_class_name method
        """
        self.assertIsNot(
            TestConsole.test_update_missing_class_name.__doc__,
            None,
            "update_missing_class_name method needs a docstring")
        self.assertTrue(len(TestConsole.test_update_missing_class_name.__doc__)
                        >= 1, "update_missing_class_name method needs a docstring")


if __name__ == "__main__":
    unittest.main()
