#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
import json


@app_views.route('/status')
def index():
    response = {"status": "OK"}
    return jsonify(response)
