#!/usr/bin/python3
"""Reviews API v1 views module"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """This function retrieves a list of all Review objects."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """This function retrieves a Review object with the id linked to it."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """This function deletes a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """This function creates a Review object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req_obj = request.get_json()
    if req_obj is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_obj.keys():
        abort(400, 'Missing user_id')

    user = storage.get(User, req_obj['user_id'])
    if user is None:
        abort(404)
    if 'text' not in req_obj.keys():
        abort(400, 'Missing text')
    req_obj['place_id'] = place_id
    review = Review(**req_obj)
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """This function updates a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req_obj = request.get_json()
    if req_obj is None:
        abort(400, 'Not a JSON')
    for key, value in req_obj.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
