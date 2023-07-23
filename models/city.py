#!/usr/bin/python3
"""The City class module"""

from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel


class City(BaseModel, Base):
    """City class definition"""

    __tablename__ = 'cities'

    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes city's object instance"""
        super().__init__(*args, **kwargs)
