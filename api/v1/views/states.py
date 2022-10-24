#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify
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
    if res is None:
        abort(404)
    return jsonify(response.to_dict())
