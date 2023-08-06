#!/usr/bin/python3
"""
This module defines the Review class, representing a review entity in the database.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Review(BaseModel, Base):
    """
    Represents a review object for the MySQL database.

    Inherits from BaseModel and links to the MySQL table 'reviews'.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store reviews.
        id (str): The primary key column. Change to String(60).
        text (str): The description of the review.
        place_id (str): The place id associated with the review.
        user_id (str): The user id associated with the review.
        created_at (datetime): The date and time of review creation.
        updated_at (datetime): The date and time of review last update.
    """

    __tablename__ = "reviews"
    id = Column(String(60), primary_key=True, nullable=False)
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    __table_args__ = {'mysql_charset': 'latin1'}

    def save(self):
        """
        Updates the updated_at attribute and saves the Review instance.

        This method updates the updated_at attribute with the current datetime
        and then calls the save() method of the BaseModel class to save the instance
        to the database.
        """
        self.updated_at = datetime.utcnow()
        super().save()

    def to_dict(self):
        """
        Returns a dictionary representation of the Review instance.

        This method returns a dictionary containing all attributes of the Review instance.
        It also includes the '__class__' key to indicate the class name of the object.
        """
        review_dict = super().to_dict()
        review_dict["text"] = self.text
        review_dict["place_id"] = self.place_id
        review_dict["user_id"] = self.user_id
        return review_dict
