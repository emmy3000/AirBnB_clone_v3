#!/usr/bin/python3
"""
This module defines the User class, representing a user entity in the database.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from hashlib import md5


class User(BaseModel, Base):
    """
    Represents User class for the MySQL database.

    Inherits from BaseModel and links to the MySQL table 'users'.

    Attributes:
        __tablename__ (str): The name of the MySQL table for users.
        id (str): The user's id (primary key).
        email (str): The user's email address.
        password (str): The user's password.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        created_at (DateTime): Datetime when the user is created.
        updated_at (DateTime): Datetime when the user is updated.
        places (relationship): User-Place relationship.
        reviews (relationship): User-Review relationship.
    """

    __tablename__ = "users"
    id = Column(String(60), primary_key=True, nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)

    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")

    __table_args__ = {'mysql_charset': 'latin1'}

    def save(self):
        """
        Updates updated_at attribute and saves the instance.

        If the password is not hashed (less than 32 characters), it will be hashed.
        """
        if self.password and len(str(self.password)) < 32:
            self.password = md5(self.password.encode()).hexdigest()
        super().save()

    def to_dict(self):
        """
        Return a dictionary representation of the User object.

        Returns:
            dict: Dictionary representation of the User object.
        """
        user_dict = super().to_dict()
        user_dict["email"] = self.email
        user_dict["password"] = self.password
        user_dict["first_name"] = self.first_name
        user_dict["last_name"] = self.last_name
        user_dict["created_at"] = self.created_at.isoformat()
        user_dict["updated_at"] = self.updated_at.isoformat()
        return user_dict
