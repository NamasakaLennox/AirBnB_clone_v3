#!/usr/bin/python3
"""This module creates the Flask app and imports the blueprint from the
    api.v1.views.index module.
"""
from api.v1.views import app_views
from flask import Flask
from os import getenv
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_db(exception):
    """This function closes the database session."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """This function handles 404 errors."""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
