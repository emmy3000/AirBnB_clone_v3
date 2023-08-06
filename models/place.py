#!/usr/bin/python3
"""
This module defines the Place class, representing a place entity in the database.
"""

from os import getenv
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel

association_table = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id", String(60), ForeignKey("places.id"),
        primary_key=True, nullable=False
    ),
    Column(
        "amenity_id", String(60), ForeignKey("amenities.id"),
        primary_key=True, nullable=False
    ),
    mysql_charset="latin1"
)


class Place(BaseModel, Base):
    """
    Represents a Place entity in the database.

    Attributes:
        __tablename__ (str): The name of the table for storing Place objects.
        id (str): The unique identifier for a Place.
        city_id (str): The foreign key to the cities table.
        user_id (str): The foreign key to the users table.
        name (str): The name of the place.
        description (str): Description of the place.
        number_rooms (int): Number of rooms in the place.
        number_bathrooms (int): Number of bathrooms in the place.
        max_guest (int): Maximum number of guests.
        price_by_night (int): Price per night for the place.
        latitude (float): Latitude of the place.
        longitude (float): Longitude of the place.
        reviews (sqlalchemy.orm.relationship): Place-Review relationship.
        amenities (sqlalchemy.orm.relationship): Place-Amenity relationship.
    """

    __tablename__ = "places"
    id = Column(String(60), primary_key=True, nullable=False)
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship(
        "Amenity",
        secondary="place_amenity",
        backref="place_amenities",
        viewonly=False
    )

    __table_args__ = {'mysql_charset': 'latin1'}

    def __init__(self, *args, **kwargs):
        """
        Initializes a new Place object.

        Args:
            *args: Variable length argument list.
            **kwargs: Keyword arguments for setting attributes.
        """
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        """
        Get a list of all linked Review instances.

        Returns:
            list: List of linked Review objects.
        """
        review_list = [
            review for review in list(storage.all(Review).values())
            if review.place_id == self.id
        ]
        return review_list

    @property
    def amenities(self):
        """
        Get/set linked Amenities.

        Returns:
            list: List of linked Amenity objects.
        """
        amenity_list = [
            amenity for amenity in list(storage.all(Amenity).values())
            if amenity.id in self.amenity_ids
        ]
        return amenity_list

    @amenities.setter
    def amenities(self, value):
        """
        Set linked Amenities.

        Args:
            value (Amenity): Amenity object to be linked.
        """
        if isinstance(value, Amenity):
            self.amenity_ids.append(value.id)
