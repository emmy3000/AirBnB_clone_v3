#!/usr/bin/python3
"""
Users API endpoints.

This module contains API endpoints for handling User objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects.

    :return: JSON response containing the list of all users.
    :rtype: Response
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users/<string:user_id>",
                 strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object with a given ID.

    :param user_id: ID of the User.
    :type user_id: str
    :return: JSON response containing the User information.
    :rtype: Response
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict()), 200


@app_views.route("/users/<string:user_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object with a given ID.

    :param user_id: ID of the User.
    :type user_id: str
    :return: Empty JSON response.
    :rtype: Response
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def create_user():
    """
    Creates a new User object.

    :return: JSON response containing the created User information.
    :rtype: Response
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")

    if not email:
        abort(400, description="Missing email")
    if not password:
        abort(400, description="Missing password")

    user = User(email=email, password=password)

    if isinstance(first_name, str) and first_name:
        user.first_name = first_name
    if isinstance(last_name, str) and last_name:
        user.last_name = last_name

    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<string:user_id>",
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object with a given ID.

    :param user_id: ID of the User.
    :type user_id: str
    :return: JSON response containing the updated User information.
    :rtype: Response
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    data = {
        k: v for k,
        v in data.items() if k not in [
            'id',
            'created_at',
            'updated_at',
            'email']}
    for k, v in data.items():
        setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict()), 200
