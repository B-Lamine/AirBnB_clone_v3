#!/usr/bin/python3
""" index page app ??
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ Return status.
    """
    return jsonify({"status": "OK"}, mimetype='application/json')
