#!/usr/bin/python3
"""DBStorage Engine Module.

This module defines the DBStorage engine used for database storage.
It provides methods for querying, adding, and deleting objects
from the database.

Classes:
    DBStorage: Represents the database storage engine.
"""

from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
import pymysql


class DBStorage:
    """
    Represents the database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): SQLAlchemy engine
            for database connection.
        __session (sqlalchemy.Session): SQLAlchemy session
            to interact with the database.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance.

        The constructor creates a new database engine
        and sets up the session.
        If the environment is set to 'test', it drops all tables
        and recreates them.
        """
        self.__engine = create_engine("mysql+pymysql://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
            Base.metadata.create_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the database.

        Args:
            cls (str or SQLAlchemy class, optional): Class to query.
                Defaults to None, which retrieves all objects from all classes.

        Returns:
            dict: A dictionary of objects with format '{ClassName}.{object_id}'.
        """
        if cls is None:
            objs = []
            for model in [State, City, User, Place, Review, Amenity]:
                objs.extend(self.__session.query(model).all())
        elif isinstance(cls, str):
            cls = eval(cls)
            objs = self.__session.query(cls).all()
        else:
            objs = self.__session.query(cls).all()

        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add a new object to the current database session.

        Args:
            obj (BaseModel): The object to add to the session.
        """
        self.__session.add(obj)

    def get(self, cls, id):
        """Retrieve an object based on class and ID"""
        key = "{}.{}".format(cls.__name__, id)
        return self.all(cls).get(key, None)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            return self.__session.query(cls).count()
        return sum(self.__session.query(model).count()
                   for model in [State, City, User, Place, Review, Amenity])

    def save(self):
        """Commit changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database session.

        Args:
            obj (BaseModel, optional): The object to delete from the session.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the current session."""
        self.__session.remove()

    def _session(self):
        """Get a new scoped session."""
        if self.__session is None:
            session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
            self.__session = scoped_session(session_factory)
        return self.__session()


# Create an instance of DBStorage
storage = DBStorage()
# Load the data from the database
storage.reload()
