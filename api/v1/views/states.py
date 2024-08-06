#!/usr/bin/python3
""" View for States objects.
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """ Get list of all states.
    """
    response = []
    objs_dict = storage.all(State)
    for obj in objs_dict.values():
        response.append(obj.to_dict())
    return jsonify(response)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """ Get state by id.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """ Delete state by id.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """ Create state.
    """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(request.json.get('name'))
    state.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ Update state by id.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            state[key] = value
    storage.save()
    return jsonify(state.to_dict()), 200
