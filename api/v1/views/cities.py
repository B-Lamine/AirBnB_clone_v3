#!/usr/bin/python3
""" View for city objects.
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ Get list of all cities of ID'ed state.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = storage.all(City).values()
    response = []
    for city_obj in all_cities:
        if state_id == city_obj.state_id:
            response.append(city_obj.to_dict())
    return jsonify(response), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """ Get city by id.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """ Delete city by id.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """ Create city.
    """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    kwargs = {'name': request.json.get('name'),
              'state_id': state_id}
    city = City(**kwargs)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ Update city by id.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
