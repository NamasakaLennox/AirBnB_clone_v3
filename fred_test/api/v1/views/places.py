#!/usr/bin/python3
"""This module creates a new view for Place objects that handles all default
    RestFul API actions.
    Routes (api/v1/):
    -----------------
        - /cities/<city_id>/places (GET, POST)
        - /places/<place_id> (GET, DELETE, PUT)
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def city_places(city_id):
    """This function returns a JSON response."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieve place with id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete(place_id):
    """delete place with id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """post place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    place = Place(**request.get_json())
    place.city_id = city_id
    storage.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """This function updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def search_place():
    """This function retrieves all Place objects depending of the JSON
    in the body of the request.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    places = storage.all(Place).values()
    api_places = []
    if len(request.get_json()) == 0:
        return jsonify([place.to_dict() for place in storage.all(Place).values()])

    if 'states' in request.get_json() and len(request.get_json()['states']) > 0:
        for place in places:
            city = storage.get(City, place.city_id)
            if city.state_id in request.get_json()['states']:
                api_places.append(place)

    if 'cities' in request.get_json() and len(request.get_json()['cities']) > 0:
        print(places)
        api_places + [place for place in places if place.city_id in
                  request.get_json()['cities']]

    if 'amenities' in request.get_json() and len(request.get_json()['amenities']) > 0:
        api_places + [place for place in places if all(amenity.id in
                  [amenity.id for amenity in place.amenities] for amenity in
                  request.get_json()['amenities'])]

    return jsonify([place.to_dict() for place in api_places if place])
