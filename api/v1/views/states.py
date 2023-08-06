#!/usr/bin/python3
"""
State API endpoints.

This module contains API endpoints for handling State objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def get_states():
    """
    Retrieves the list of all State objects.

    :return: JSON response containing the list of all states.
    :rtype: Response
    """
    states = list(storage.all(State).values())
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<string:state_id>",
                 strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """
    Retrieves a State object with a given ID.

    :param state_id: ID of the State.
    :type state_id: str
    :return: JSON response containing the State information.
    :rtype: Response
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict()), 200

    return jsonify({'error': 'Not found'}), 404


@app_views.route("/states/<string:state_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object with a given ID.

    :param state_id: ID of the State.
    :type state_id: str
    :return: Empty JSON response.
    :rtype: Response
    """
    state = storage.get(State, state_id)
    if state:
        state.delete()
        return jsonify({}), 200

    return jsonify({'error': 'Not found'}), 404


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def create_state():
    """
    Creates a new State object.

    :return: JSON response containing the created State information.
    :rtype: Response
    """
    if request.is_json:
        data = request.get_json()
        state_name = data.get('name', None)
        if state_name:
            state = State(name=state_name)
            state.save()
            return jsonify(state.to_dict()), 201

        abort(400, description='Missing name')

    abort(400, description='Not a JSON')


@app_views.route("/states/<string:state_id>",
                 strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """
    Updates a State object with a given ID.

    :param state_id: ID of the State.
    :type state_id: str
    :return: JSON response containing the updated State information.
    :rtype: Response
    """
    if request.is_json:
        state = storage.get(State, state_id)
        if state:
            data = request.get_json()
            data = {
                k: v for k,
                v in data.items() if k not in [
                    'id',
                    'created_at',
                    'updated_at']}
            for k, v in data.items():
                setattr(state, k, v)

            state.save()
            updated_state = storage.get(State, state_id)
            return jsonify(updated_state.to_dict()), 200

        abort(404)

    abort(400, description='Not a JSON')
