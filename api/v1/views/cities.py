#!/usr/bin/python3
"""
City API endpoints.

This module contains API endpoints for handling City objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities",
                 strict_slashes=False, methods=['GET'])
def get_state_cities(state_id):
    """
    Retrieves all city objects in a state.

    :param state_id: ID of the State.
    :type state_id: str
    :return: JSON response containing the list of cities in the state.
    :rtype: Response
    """
    state = storage.get(State, state_id)
    if state is not None:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>",
                 strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """
    Retrieves a city with a given ID.

    :param city_id: ID of the City.
    :type city_id: str
    :return: JSON response containing the city information.
    :rtype: Response
    """
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a city with a given ID.

    :param city_id: ID of the City.
    :type city_id: str
    :return: Empty JSON response.
    :rtype: Response
    """
    city = storage.get(City, city_id)
    if city is not None:
        city.delete()
        return jsonify({})
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/states/<string:state_id>/cities",
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """
    Creates a city in the specified state.

    :param state_id: ID of the State.
    :type state_id: str
    :return: JSON response containing the created city information.
    :rtype: Response
    """
    state = storage.get(State, state_id)
    if state is not None:
        if request.is_json:
            data = request.get_json()
            city_name = data.get('name', None)
            if city_name is None:
                return jsonify({'error': 'Missing name'}), 400
            city = City(name=city_name, state_id=state_id)
            city.save()
            return jsonify(city.to_dict()), 201
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>",
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """
    Updates a city with a given ID.

    :param city_id: ID of the City.
    :type city_id: str
    :return: JSON response containing the updated city information.
    :rtype: Response
    """
    city = storage.get(City, city_id)
    if city is not None:
        if request.is_json:
            data = request.get_json()
            update_data = {}
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    update_data[k] = v

            for k, v in update_data.items():
                setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict()), 200
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404
