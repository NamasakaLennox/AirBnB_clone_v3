#!/usr/bin/python3
"""Module that contains link between Place objects and Amenity objects that
 handles all default RESTFul API actions:
"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenity(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, id).to_dict()
                     for id in place.amenity_ids]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_amenity_delete(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def place_amenity_post(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
