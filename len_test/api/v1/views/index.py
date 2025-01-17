#!/usr/bin/python3
"""
index file
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """returns the status of the app
    """
    obj = {"status": "OK"}
    return (jsonify(obj))


@app_views.route('/stats')
def count():
    """
    counts the numbrer of objects in the database
    """
    keys = classes.keys()
    values = classes.values()
    obj = {}
    for key, val in zip(keys, values):
        num = storage.count(val)
        obj[key] = num

    return (jsonify(obj))
