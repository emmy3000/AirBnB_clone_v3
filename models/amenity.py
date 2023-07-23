#!/usr/bin/python3
"""The Amenity class module"""

from models.base_model import Base
from sqlalchemy import Column, String, Integer


class Amenity(Base):
    """Represents Amenity class for MySQL database.

    Inherits from SQLAlchemy Base & links to MySQL amenities table.

    Attributes:
        __tablename__ (str): name of MySQL table for storing Amenities.
        id (sqlalchemy Integer): primary key column.
        name (sqlalchemy String): amenity's name.
    """

    __tablename__ = "amenities"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
