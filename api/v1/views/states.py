#!/usr/bin/python3
"""Module for State objects that handles all default RestFul API actions.
   Routes (api/v1/):
   ----------------
        - /states (GET, POST)
        - /states/<state_id> (GET, DELETE, PUT)
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """This function returns a JSON response."""
    states = storage.all(State).values()
    states_json = [state.to_dict() for state in states]
    return jsonify(states_json)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states_id(state_id):
    """This function retrieves a State object with the id linked to it."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """This function deletes a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def post_state():
    """This function creates a State object."""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """This function updates a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
