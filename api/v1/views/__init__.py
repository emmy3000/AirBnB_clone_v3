#!/usr/bin/python3
"""
This is the __init__.py file for the 'app_views' Blueprint.

It defines the routes and imports views for the API's version 1.

Routes:
    - /api/v1/        (index)
    - /api/v1/states
    - /api/v1/cities
    - /api/v1/places
    - /api/v1/places_reviews
    - /api/v1/amenities
    - /api/v1/users
    - /api/v1/places_amenities
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views after app_views is defined
from api.v1.views.places_amenities import *
from api.v1.views.users import *
from api.v1.views.amenities import *
from api.v1.views.places_reviews import *
from api.v1.views.places import *
from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.index import *
