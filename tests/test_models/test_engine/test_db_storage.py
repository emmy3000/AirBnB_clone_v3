#!/usr/bin/python3
"""Test DBStorage Engine Module.

This module defines the Test DBStorage engine used
for database storage.
"""

import unittest
import os
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.state import State
from models.city import City


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing DBStorage only")
class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage class"""

    def setUp(self):
        """Set up the test environment"""
        # Replace with your database configurations
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db_name = os.getenv("HBNB_MYSQL_DB")

        self.db_storage = DBStorage()
        self.db_storage.reload()

    def tearDown(self):
        """Teardown the test environment"""
        self.db_storage.close()

    def test_all(self):
        """Test the 'all' method of DBStorage"""
        # Add some test data to the database
        state = State(name="California")
        city = City(name="San Francisco", state_id=state.id)
        self.db_storage.new(state)
        self.db_storage.new(city)
        self.db_storage.save()

        # Get all objects using the 'all' method
        all_objs = self.db_storage.all()

        # Make sure the objects were retrieved correctly
        self.assertIn("State.{}".format(state.id), all_objs)
        self.assertIn("City.{}".format(city.id), all_objs)

    def test_new_save(self):
        """Test the 'new' and 'save' methods of DBStorage"""
        # Add a new object to the database
        state = State(name="New York")
        self.db_storage.new(state)
        self.db_storage.save()

        # Check if the object was saved correctly in the database
        state_key = "State.{}".format(state.id)
        all_objs = self.db_storage.all()
        self.assertIn(state_key, all_objs)

    def test_delete(self):
        """Test the 'delete' method of DBStorage"""
        # Add an object to the database
        state = State(name="Texas")
        self.db_storage.new(state)
        self.db_storage.save()

        # Delete the object and check if it's removed from the database
        state_key = "State.{}".format(state.id)
        self.assertIn(state_key, self.db_storage.all())

        self.db_storage.delete(state)
        self.db_storage.save()
        self.assertNotIn(state_key, self.db_storage.all())

    def test_reload(self):
        """Test the 'reload' method of DBStorage"""
        original_session = self.db_storage._DBStorage__session

        self.db_storage.reload()
        reloaded_session = self.db_storage._DBStorage__session

        # Make sure the session is reloaded and not the same as the original
        self.assertIsNot(original_session, reloaded_session)
        self.assertIsNone(self.db_storage._DBStorage__session)

