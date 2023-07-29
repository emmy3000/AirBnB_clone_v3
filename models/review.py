#!/usr/bin/python3
"""The Review class module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """Represents a review object for MySQL database.

    Inherits from BaseModel & links to the MySQL table 'reviews'.

    Attributes:
        __tablename__ (str): name of the MySQL table to store reviews.
        id (sqlalchemy String): primary key column. Change to String(60).
        text (sqlalchemy String): review class' description.
        place_id (sqlalchemy String): review class' place id.
        user_id (sqlalchemy String): review class' user id.
    """
    __tablename__ = "reviews"
    id = Column(String(60), primary_key=True, nullable=False)
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    __table_args__ = {'mysql_charset': 'latin1'}

    def save(self):
        """Updates updated_at attribute and saves the instance"""
        super().save()

    def to_dict(self):
        """Returns a dictionary representation of Review"""
        review_dict = super().to_dict()
        review_dict["text"] = self.text
        review_dict["place_id"] = self.place_id
        review_dict["user_id"] = self.user_id
        return review_dict
