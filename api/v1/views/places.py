#!/usr/bin/python3
""" View for place objects.
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """ Get list of all places of ID'ed city.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = storage.all(Place).values()
    response = []
    for place_obj in all_places:
        if city_id == place_obj.city_id:
            response.append(place_obj.to_dict())
    return jsonify(response), 200


@app_views.route('places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """ Get place by id.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """ Delete place by id.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """ Create place.
    """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user = storage.get(User, request.json.get('user_id'))
    if user is None:
        abort(404)
    kwargs = {'name': request.json.get('name'),
              'user_id': request.json.get('user_id'),
              'city_id': city_id}
    place = Place(**kwargs)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ Update place by id.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
