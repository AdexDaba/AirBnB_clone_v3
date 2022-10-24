#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from api.vi import app
from models import storage
from models.base_model import BaseModel, Base
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """ address to display all states """
    response = []
    states = storage.all(State)
    for state in states.values():
        response.append(state.to_dict())
    return jsonify(response)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_by_id(state_id):
    """ address to display state by id """
    response = storage.get(State, state_id)
    if response is None:
        app.abort(404)
    return jsoniify(response.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                strict_slashes=False)
def del_state(state_id=None):
    """ delete state by id """
    if state_id is None:
        app.abort(404)
    else:
        trash = storage.get(State, state_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            app.abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a new state """
    new = request.get_json()
    if new is None or type(new) is not dict:
        abort(400, description='Not a JSON')
    if 'name' not in new.keys():
        abort(400, description='Missing name')
    response = State(**new)
    response.save()
    return make_response(jsonify(response.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """ update an existing state """
    response = storage.get(State, state_id)
    if state_id is None or response is None:
        abort(404)
    new = request.get_json()
    if new is None or type(new) is not dict:
        abort(400, description='Not a JSON')
    for key in new.keys():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(response, key, new[key])
    response.save()
    return make_response(jsonify(response.to_dict()), 200)
