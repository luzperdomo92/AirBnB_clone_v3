#!/usr/bin/python3
"""Object that returns a JSON response"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Jsonify the response and returns it"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ retrieves the number of each objects by type"""
    objects_by_type = {"amenities": storage.count(Amenity),
                       "cities": storage.count(City),
                       "places": storage.count(Place),
                       "reviews": storage.count(Review),
                       "states": storage.count(State),
                       "users": storage.count(User)}
    return jsonify(objects_by_type)
