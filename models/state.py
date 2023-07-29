#!/usr/bin/python3
"""The State class module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """Represents State class for MySQL database.

    Inherits from SQLAlchemy Base & links to MySQL table states.

    Attributes:
        __tablename__ (str): name of MySQL table for storing states.
        name (sqlalchemy String): name of state.
        cities (sqlalchemy relationship): State-City relationship.
    """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    __table_args__ = {'mysql_charset': 'latin1'}

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def cities(self):
            """Get a list of all related City objects."""
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
        """Return a dictionary representation of the State instance."""
        state_dict = super().to_dict()
        state_dict["name"] = self.name
        return state_dict
