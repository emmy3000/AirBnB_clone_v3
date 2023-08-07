#!/usr/bin/python3
"""
This module defines the City class, representing a city entity in the database.
"""

import re
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel


class City(BaseModel, Base):
    """
    City class representing a city entity in the database.

    Attributes:
        __tablename__ (str): The name of the table for storing City objects.
        state_id (sqlalchemy String): The foreign key to the states table.
        name (sqlalchemy String): The name of the city.
        __table_args__ (dict): Additional arguments for the SQLAlchemy table.

    Note:
        The `__table_args__` attribute is used to specify additional options for the SQLAlchemy
        table, such as the charset. In this class, we use it to set the MySQL charset to 'latin1'
        to ensure compatibility with the existing database.
    """

    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)

    # Add the __table_args__ attribute for specifying the charset
    __table_args__ = {'mysql_charset': 'latin1'}

    def __init__(self, *args, **kwargs):
        """
        Initializes a new City object.

        Args:
            *args: Variable length argument list.
            **kwargs: Keyword arguments for setting attributes.
        """
        super().__init__(*args, **kwargs)

        # Handle the state_id manually if provided
        if 'state_id' in kwargs:
            state_id = kwargs['state_id']
            if not re.match(
                r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                    state_id):
                raise ValueError("Invalid state_id format")
            self.state_id = state_id

        # Debugging statements
        print("State ID before save:", self.state_id)
