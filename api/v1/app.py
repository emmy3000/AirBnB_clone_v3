#!/usr/bin/python3
"""
This script serves as the main entrance to the API.
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_database_session(exception):
    """
    Closes the database session after the context is torn down.

    Args:
        exception (Exception): The exception that caused the teardown.
    """
    storage.close()


@app.errorhandler(404)
def handle_not_found(error):
    """
    Handles 404 error by returning a JSON response.

    Args:
        error (HTTPException): The error that occurred.

    Returns:
        Response: A JSON response containing the error message and status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def handle_bad_request(error):
    """
    Handles 400 error by returning a JSON response.

    Args:
        error (HTTPException): The error that occurred.

    Returns:
        Response: A JSON response containing the error message and status code.
    """
    return jsonify({"error": error.description}), 400


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', '5000')),
        threaded=True
    )
