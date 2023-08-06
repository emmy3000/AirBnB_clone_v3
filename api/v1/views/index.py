#!/usr/bin/python3
"""
Index page of the website.

This module contains API endpoints for the index page of the website.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping endpoints to their respective model classes
endpoints_dict = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route("/status", strict_slashes=False)
def status():
    """
    Handles the status route.

    :return: JSON response containing the status message.
    :rtype: Response
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """
    Handles the stats route.

    :return: JSON response containing the count of objects for each endpoint.
    :rtype: Response
    """
    stats_data = {}
    for endpoint, model_class in endpoints_dict.items():
        stats_data[endpoint] = storage.count(model_class)
    return jsonify(stats_data)


if __name__ == "__main__":
    pass
