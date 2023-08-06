#!/usr/bin/python3
"""
Place API endpoints.

This module contains API endpoints for handling Place objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<string:city_id>/places",
                 strict_slashes=False, methods=['GET'])
def get_city_places(city_id):
    """
    Retrieves all Place objects in a city.

    :param city_id: ID of the City.
    :type city_id: str
    :return: JSON response containing the list of places in the city.
    :rtype: Response
    """
    city = storage.get(City, city_id)
    if city is not None:
        places_list = []
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>",
                 strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place with a given ID.

    :param place_id: ID of the Place.
    :type place_id: str
    :return: JSON response containing the place information.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place with a given ID.

    :param place_id: ID of the Place.
    :type place_id: str
    :return: Empty JSON response.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        return jsonify({})
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>/places",
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """
    Creates a Place in the specified city.

    :param city_id: ID of the City.
    :type city_id: str
    :return: JSON response containing the created place information.
    :rtype: Response
    """
    city = storage.get(City, city_id)
    if city is not None:
        if request.is_json:
            data = request.get_json()
            user_id = data.get('user_id')
            place_name = data.get('name')
            longitude = data.get('longitude')
            latitude = data.get('latitude')
            description = data.get('description')
            number_rooms = data.get('number_rooms', 0)
            number_bathrooms = data.get('number_bathrooms', 0)
            max_guest = data.get('max_guest', 0)
            price_by_night = data.get('price_by_night', 0)

            if not user_id:
                return jsonify({'error': 'Missing user_id'}), 400

            user = storage.get(User, user_id)
            if not user:
                return jsonify({'error': 'Not found'}), 404

            if not place_name:
                return jsonify({'error': 'Missing name'}), 400

            place = Place(
                user_id=user_id,
                city_id=city_id,
                name=place_name,
                number_rooms=number_rooms,
                number_bathrooms=number_bathrooms,
                max_guest=max_guest,
                price_by_night=price_by_night
            )

            if latitude:
                place.latitude = float(latitude)

            if longitude:
                place.longitude = float(longitude)

            if description:
                place.description = description

            place.save()
            return jsonify(place.to_dict()), 201
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>",
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place with a given ID.

    :param place_id: ID of the Place.
    :type place_id: str
    :return: JSON response containing the updated place information.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if place is not None:
        if request.is_json:
            data = request.get_json()
            data = {
                k: v for k,
                v in data.items() if k not in [
                    'id',
                    'created_at',
                    'updated_at',
                    'user_id',
                    'city_id']}
            for k, v in data.items():
                setattr(place, k, v)
            place.save()
            return jsonify(place.to_dict()), 200
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/places_search", strict_slashes=False, methods=['POST'])
def places_search():
    """
    Retrieves all Place objects based on the JSON data in the request body.

    :return: JSON response containing the list of places based on the search criteria.
    :rtype: Response
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])
    places = []

    if not states and not cities and not amenities:
        places = list(storage.all(Place).values())

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
                    if city.id in cities:
                        cities.remove(city.id)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    if amenities:
        for place in places.copy():
            if len(amenities) != len(place.amenities):
                places.remove(place)
            else:
                for amenity in place.amenities:
                    if amenity.id not in amenities:
                        places.remove(place)
                        break

    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)
