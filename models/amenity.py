#!/usr/bin/python3
"""The Amenity class module"""

from datetime import datetime
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer


class Amenity(BaseModel, Base):
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

    def __init__(self, *args, **kwargs):
        """Initialize Amenity object.

        Call parent's (BaseModel's) __init__ to apply BaseModel behavior.
        """
        super().__init__(*args, **kwargs)

    def save(self):
        """Save the current instance to the database."""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the Amenity instance."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "__class__": self.__class__.__name__,
        }
