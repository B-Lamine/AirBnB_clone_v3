#!/usr/bin/python3
""" index page.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place
from models.user import User

classes = [Amenity, City, Review, State, Place, User]


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ Return status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """ Stats for stored objects.
    """
    stats = {}
    for cls in classes:
        stats.update({cls.__name__: storage.count(cls)})
    return jsonify(stats)
