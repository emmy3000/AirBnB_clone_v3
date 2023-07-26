#!/usr/bin/python3
"""The Review class module"""

from models.base_model import Base
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


class Review(Base):
    """Represents a review object for MySQL database.

    Inherits from SQLAlchemy Base & links the MySQL table review objects.

    Attributes:
        __tablename__ (str): name of the MySQL table to store Reviews.
        id (sqlalchemy String): primary key column. Change to String(60).
        text (sqlalchemy String): review class' description.
        place_id (sqlalchemy String): review class' place id.
        user_id (sqlalchemy String): review class' user id.
    """
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    __table_args__ = {'mysql_charset': 'latin1'}
