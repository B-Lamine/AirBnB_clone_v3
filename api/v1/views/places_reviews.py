#!/usr/bin/python3
""" View for places' reviews.
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """ Get list of all reviews of ID'ed place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_reviews = storage.all(Review).values()
    response = []
    for review_obj in all_reviews:
        if review_id == review_obj.place_id:
            response.append(review_obj.to_dict())
    return jsonify(response), 200


@app_views.route('reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ Get review by id.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """ Delete review by id.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """ Create review.
    """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in request.json:
        return make_response(jsonify({"error": "Missing text"}), 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    user = storage.get(User, request.json.get('user_id'))
    if user is None:
        abort(404)
    kwargs = {'name': request.json.get('name'),
              'user_id': request.json.get('user_id'),
              'text': request.json.get('text'),
              'place_id': place_id}
    review = Review(**kwargs)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """ Update review by id.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
