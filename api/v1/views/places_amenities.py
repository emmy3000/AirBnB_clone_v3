#!/usr/bin/python3
"""
Places Amenities API endpoints.

This module contains API endpoints for handling Amenities of Places.
"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False, methods=['GET'])
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects linked to a Place.

    :param place_id: ID of the Place.
    :type place_id: str
    :return: JSON response containing the list of amenities linked to the Place.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object linked to a Place.

    :param place_id: ID of the Place.
    :type place_id: str
    :param amenity_id: ID of the Amenity.
    :type amenity_id: str
    :return: Empty JSON response.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == 'db':
        found_amenities = list(
            filter(
                lambda d: d.id == amenity_id,
                place.amenities))
    else:
        found_amenities = list(
            filter(
                lambda id: id == amenity_id,
                place.amenity_ids))

    if not found_amenities:
        abort(404)

    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)

    place.save()
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def link_amenity_place(place_id, amenity_id):
    """
    Links an Amenity object to a Place.

    :param place_id: ID of the Place.
    :type place_id: str
    :param amenity_id: ID of the Amenity.
    :type amenity_id: str
    :return: JSON response containing the linked Amenity information.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == 'db':
        found_amenities = list(
            filter(
                lambda d: d.id == amenity_id,
                place.amenities))
    else:
        found_amenities = list(
            filter(
                lambda id: id == amenity_id,
                place.amenity_ids))

    if len(found_amenities) == 1:
        return jsonify(amenity.to_dict()), 200

    if storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)

    place.save()
    return jsonify(amenity.to_dict()), 201
