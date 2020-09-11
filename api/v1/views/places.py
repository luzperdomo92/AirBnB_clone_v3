#!/usr/bin/python3
"""View for Place objects that handles different RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_in_city(city_id):
    """Method to retrieve the list of all places in a city.
       It also creates a city on the state if requested"""
    city = fetch_city(city_id)

    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place_in_city(city_id):
    """Method to create a Place in a City"""
    city = fetch_city(city_id)

    request_dict = request.get_json()
    if not request_dict:
        abort(400, 'Not a JSON')

    if 'user_id' not in request_dict:
        abort(400, 'Missing user_id')

    # raise 404 if not found
    fetch_user(request_dict['user_id'])

    if 'name' not in request_dict or not request_dict['name']:
        abort(400, 'Missing name')

    new_place = Place(**request_dict)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


def fetch_city(city_id):
    """fetch_city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    return city


def fetch_user(user_id):
    """fetch_city"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    return user


@app_views.route('/places/<place_id>', methods=['GET'])
def retrieve_place(place_id):
    """Retrieves a place"""
    # raise 404 if not found
    place = fetch_place(place_id)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Destroy a Place"""
    # raise 404 if not found
    place = fetch_place(place_id)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400, 'Not a JSON')

    # raise 404 if not found
    place = fetch_place(place_id)
    for key, value in request_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


def fetch_place(place_id):
    """fetch_place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    return place
