#!/usr/bin/python3
""" HBnB API.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Close session if DB storage, load objects if file storage.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ JSON response for 404 errors.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    hbnb_api_host = os.getenv('HBNB_API_HOST')
    hbnb_api_port = os.getenv('HBNB_API_PORT')
    host = hbnb_api_host if hbnb_api_host else '0.0.0.0'
    port = hbnb_api_port if hbnb_api_port else 5000
    app.run(host=host, port=port, threaded=True)
