#!/usr/bin/python3
"""Object that returns a JSON response"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def response():
    """Jsonify the response and returns it"""
    return jsonify("status": "OK")
