#!/usr/bin/python3
"""
This module defines the State class, representing a state entity in the database.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """
    Represents State class for the MySQL database.

    Inherits from BaseModel and links to the MySQL table 'states'.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store states.
        name (str): The name of the state.
        cities (relationship): State-City relationship.
    """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    __table_args__ = {'mysql_charset': 'latin1'}

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def cities(self):
            """
            Get a list of all related City objects.

            Returns:
                list: List of City objects related to the state.
            """
            from models import storage
            city_list = [
                city for city in list(storage.all(City).values())
                if city.state_id == self.id
            ]
            return city_list

    else:
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")

    def to_dict(self):
        """
        Return a dictionary representation of the State instance.

        Returns:
            dict: Dictionary representation of the State instance.
        """
        state_dict = super().to_dict()
        state_dict["name"] = self.name
        return state_dict
