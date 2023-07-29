#!/usr/bin/python3
"""The User class module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represents MySQL database for class User.

    Inherits from SQLAlchemy Base & links to MySQL table users.

    Attributes:
        __tablename__ (str): name of the MySQL table for users.
        id: (sqlalchemy String): user's id (primary key). Change to String(60).
        email: (sqlalchemy String): user's email address.
        password (sqlalchemy String): user's password.
        first_name (sqlalchemy String): user's first name.
        last_name (sqlalchemy String): user's last name.
        places (sqlalchemy-relationship): User-Place relationship.
        reviews (sqlalchemy-relationship): User-Review relationship.
    """
    __tablename__ = "users"
    id = Column(String(60), primary_key=True, nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")

    __table_args__ = {'mysql_charset': 'latin1'}

    def save(self):
        """Updates updated_at attribute and saves the instance"""
        super().save()

    def to_dict(self):
        """Return a dictionary representation of the User object."""
        user_dict = {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        return user_dict
