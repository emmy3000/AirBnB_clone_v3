#!/usr/bin/python3
"""
Amenities API endpoints.

This module contains API endpoints for Amenities.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
@app_views.route("/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=['GET'])
def get_amenities(amenity_id=None):
    """
    Retrieves the list of all Amenity objects or a specific Amenity object.

    :param amenity_id: ID of the Amenity to retrieve.
    :type amenity_id: str
    :return: JSON response containing the list of amenities or a specific amenity.
    :rtype: Response
    """
    if amenity_id is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())

    amenities = list(storage.all(Amenity).values())
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Delete an Amenity.

    :param amenity_id: ID of the Amenity to delete.
    :type amenity_id: str
    :return: Empty JSON response.
    :rtype: Response
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def create_amenity():
    """
    Create an Amenity.

    :return: JSON response containing the created amenity.
    :rtype: Response
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    name = data.get("name", None)
    if name is None:
        abort(400, description="Missing name")
    amenity = Amenity(name=name)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity.

    :param amenity_id: ID of the Amenity to update.
    :type amenity_id: str
    :return: JSON response containing the updated amenity.
    :rtype: Response
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    update_data = {}
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            update_data[k] = v

    for k, v in update_data.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
