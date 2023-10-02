#!/usr/bin/python3
"""
handles operations for the state class
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    returns all states
    """
    dict_ = []
    for val in storage.all(State).values():
        dict_.append(val.to_dict())
    return jsonify(dict_)


@app_views.route('/states/<path:state_id>')
def get_state(state_id):
    """
    returns a state that matches given id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<path:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes a state
    """
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """
    posts a new state
    """
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    new_state = State(**res)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<path:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """
    adds a new state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200