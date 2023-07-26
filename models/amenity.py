#!/usr/bin/python3
"""The Amenity class module"""

from models.base_model import Base
from sqlalchemy import Column, String, Integer


class Amenity(Base):
    """Represents Amenity class for MySQL database.

    Inherits from SQLAlchemy Base & links to MySQL amenities table.

    Attributes:
        __tablename__ (str): name of MySQL table for storing Amenities.
        id (sqlalchemy String): primary key column. Change to String(60).
        name (sqlalchemy String): amenity's name.
    """

    __tablename__ = "amenities"
    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    __table_args__ = {'mysql_default_charset': 'latin1'}
