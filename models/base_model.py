#!/usr/bin/python3
"""
Initialize the models package and create the BaseModel class.
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    The BaseModel class from which future classes will be derived.

    Attributes:
        id (str): Primary key for the database or a unique identifier.
        created_at (datetime): Date and time of object creation.
        updated_at (datetime): Date and time of last update.

    Methods:
        __init__(*args, **kwargs): Initializes the base model.
        __str__(): Returns a string representation of the BaseModel instance.
        save(): Updates the 'updated_at' attribute with the current datetime.
        to_dict(): Returns a dictionary containing all keys/values of the instance.
        delete(): Deletes the current instance from the storage.
    """

    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initializes the base model.

        Args:
            *args: Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get(
                    "created_at",
                    None) and isinstance(
                    self.created_at,
                    str):
                self.created_at = datetime.strptime(
                    kwargs["created_at"], time_format)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get(
                    "updated_at",
                    None) and isinstance(
                    self.updated_at,
                    str):
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"], time_format)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """
        Returns a string representation of the BaseModel class.

        Returns:
            str: The string representation.
        """
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime.

        Updates the object in the storage and saves it.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance.

        Returns:
            dict: A dictionary representation of the instance.
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(
                time_format)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(
                time_format)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        if "password" in new_dict and models.storage_t == "db":
            del new_dict["password"]

        return new_dict

    def delete(self):
        """
        Deletes the current instance from the storage.
        """
        models.storage.delete(self)
