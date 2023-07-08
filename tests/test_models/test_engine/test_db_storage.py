#!/usr/bin/python3
"""Unit tests for DBStorage class"""

import unittest
import pep8
import MySQLdb
import os
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'No database configuration')
class TestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test class"""
        cls.User = getenv("HBNB_MYSQL_USER")
        cls.Passwd = getenv("HBNB_MYSQL_PWD")
        cls.Db = getenv("HBNB_MYSQL_DB")
        cls.Host = getenv("HBNB_MYSQL_HOST")
        cls.db = MySQLdb.connect(host=cls.Host, user=cls.User,
                                 passwd=cls.Passwd, db=cls.Db,
                                 charset="utf8")
        cls.query = cls.db.cursor()
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class"""
        cls.query.close()
        cls.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'No database configuration')
    def test_pep8_DBStorage(self):
        """Test for PEP 8 compliance of the DBStorage module"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'No database configuration')
    def test_read_tables(self):
        """Test the existence of database tables"""
        self.query.execute("SHOW TABLES")
        result = self.query.fetchall()
        self.assertEqual(len(result), 7)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'No database configuration')
    def test_no_element_user(self):
        """Test that there are no elements in the 'users' table"""
        self.query.execute("SELECT * FROM users")
        result = self.query.fetchall()
        self.assertEqual(len(result), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'No database configuration')
    def test_no_element_cities(self):
        """Test that there are no elements in the 'cities' table"""
        self.query.execute("SELECT * FROM cities")
        result = self.query.fetchall()
        self.assertEqual(len(result), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'No database configuration')
    def test_add(self):
        """Test the consistency of the storage() method with the existing database"""
        self.query.execute("SELECT * FROM states")
        result = self.query.fetchall()
        self.assertEqual(len(result), 0)
        state = State(name="LUISILLO")
        state.save()
        self.db.autocommit(True)
        self.query.execute("SELECT * FROM states")
        result = self.query.fetchall()
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
