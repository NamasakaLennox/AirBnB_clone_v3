#!/usr/bin/python3
"""This module creates a new view for State objects that handles all default
    RestFul API actions.
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """This function returns a JSON response."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """This function returns a JSON response."""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.state import State
    from models.review import Review
    from models.user import User

    models = {"amenities": Amenity, "cities": City, "places": Place,
              "states": State, "reviews": Review, "users": User}
    model_count = {}

    for model_name, model in models.items():
        count = storage.count(model)
        model_count[model_name] = count

    return jsonify(model_count)
