#!/usr/bin/python3
""" View for users objects.
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ Get list of all users.
    """
    response = []
    objs_dict = storage.all(User)
    for obj in objs_dict.values():
        response.append(obj.to_dict())
    return jsonify(response), 200


@app_views.route('users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """ Get user by id.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """ Delete user by id.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_users():
    """ Create user.
    """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    user = User(name=request.json.get('name'))
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ Update user by id.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
