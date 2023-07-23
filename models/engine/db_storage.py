#!/usr/bin/python3
"""DBStorage Engine Module

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
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the database.

        Args:
            cls (str or SQLAlchemy class, optional):class to query.
                Defaults to None, which retrieves all objects from all classes.

        Returns:
            dict: A dictionary of objects with format \
                    '{ClassName}.{object_id}'.
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add a new object to the current database session.

        Args:
            obj (BaseModel): The object to add to the session.
        """
        self.__session.add(obj)

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
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current session."""
        self.__session.close()
