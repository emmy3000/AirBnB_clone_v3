#!/usr/bin/python3
"""
This module defines the City class, representing a city entity in the database.
"""

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
    """

    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)

    __table_args__ = {'mysql_charset': 'latin1'}

    def __init__(self, *args, **kwargs):
        """
        Initializes a new City object.

        Args:
            *args: Variable length argument list.
            **kwargs: Keyword arguments for setting attributes.
        """
        super().__init__(*args, **kwargs)
