#!/usr/bin/python3
""" index page app ??
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place
from models.user import User

classes = [Amenity, City, Review, State, Place, User]


@app_views.route('/status', methods=['GET'])
def status():
    """ Return status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ Stats for stored objects.
    """
    stats = {}
    for cls in classes:
        stats.append({cls.__name__: storage.count(cls)})
    return jsonify(stats)
