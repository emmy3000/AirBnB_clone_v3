#!/usr/bin/python3
"""
Place Reviews API endpoints.

This module contains API endpoints for handling Reviews of Places.
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<string:place_id>/reviews",
                 strict_slashes=False, methods=['GET'])
def get_place_reviews(place_id):
    """
    Retrieves the list of all Review objects linked to a Place.

    :param place_id: ID of the Place.
    :type place_id: str
    :return: JSON response containing the list of reviews linked to the Place.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())

    return jsonify(reviews), 200


@app_views.route("/reviews/<string:review_id>",
                 strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object with a given ID.

    :param review_id: ID of the Review.
    :type review_id: str
    :return: JSON response containing the Review information.
    :rtype: Response
    """
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({'error': 'Not found'}), 404

    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<string:review_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object with a given ID.

    :param review_id: ID of the Review.
    :type review_id: str
    :return: Empty JSON response.
    :rtype: Response
    """
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({'error': 'Not found'}), 404

    review.delete()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/reviews",
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """
    Creates a Review for a given Place.

    :param place_id: ID of the Place.
    :type place_id: str
    :return: JSON response containing the created Review information.
    :rtype: Response
    """
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404

    if request.is_json:
        data = request.get_json()
        user_id = data.get('user_id', None)
        text = data.get('text', None)

        if not user_id or user_id == "":
            return jsonify({'error': 'Missing user_id'}), 400

        user = storage.get(User, user_id)
        if not user:
            return jsonify({'error': 'Not found'}), 404

        if not text or text == "":
            return jsonify({'error': 'Missing text'}), 400

        review = Review(place_id=place_id, user_id=user_id, text=text)
        review.save()
        return jsonify(review.to_dict()), 201

    return jsonify({'error': 'Not a JSON'}), 400


@app_views.route("/reviews/<string:review_id>",
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object with a given ID.

    :param review_id: ID of the Review.
    :type review_id: str
    :return: JSON response containing the updated Review information.
    :rtype: Response
    """
    review = storage.get(Review, review_id)
    if review:
        if request.is_json:
            data = request.get_json()
            data = {
                k: v for k,
                v in data.items() if k not in [
                    'id',
                    'created_at',
                    'updated_at',
                    'user_id',
                    'place_id']}
            for k, v in data.items():
                setattr(review, k, v)

            review.save()
            updated_review = storage.get(Review, review_id)
            return jsonify(updated_review.to_dict()), 200

        return jsonify({'error': 'Not a JSON'}), 400

    return jsonify({'error': 'Not found'}), 404
