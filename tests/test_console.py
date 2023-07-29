#!/usr/bin/python3
"""
Unit tests for console.py
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
    """Class for testing the console"""

    @classmethod
    def setUpClass(cls):
        """Set up for the test"""
        cls.console = HBNBCommand()

    @classmethod
    def tearDown(cls):
        """Tear down the test"""
        del cls.console

    def tearDown(self):
        """Remove temporary file (file.json) created
        during the test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_console(self):
        """Test for PEP8 compliance in console.py"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(["console.py"])
        self.assertEqual(result.total_errors, 0,
                         'Fix PEP8 issues in console.py')

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(
                'create User email="hoal@.com" password="1234"'
            )

    def test_show(self):
        """Test show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue()
            )

    def test_destroy(self):
        """Test destroy command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue()
            )

    def test_all(self):
        """Test all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all asdfsdfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue()
            )

    def test_z_all(self):
        """Test alternate all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("asdfsdfsd.all()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())

    def test_z_count(self):
        """Test count command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("asdfsdfsd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    def test_z_show(self):
        """Test alternate show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue()
            )

    def test_z_destroy(self):
        """Test alternate destroy command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue()
            )

    def test_z_update(self):
        """Test alternate update command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("sldkfjsl.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue()
            )
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.update(" + my_id + ")")
            self.assertIn(
                "** attribute name missing **",
                f.getvalue()
            )


if __name__ == "__main__":
    unittest.main()
