#!/usr/bin/python3
"""View for City objects that handles different RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_in_state(state_id):
    """Method to retrieve the list of all cities in a state.
       It also creates a city on the state if requested"""
    # Gets the state by its ID
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    # Perform the GET request
    if request.method == 'GET':
        cities_list = []
        for city in state.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)

    # Perform the POST request
    if request.method == 'POST':
        request_dict = request.get_json()
        if not request_dict:
            abort(400, 'Not a JSON')
        if 'name' not in request_dict:
            abort(400, 'Missing name')
        new_city = City(**request_dict)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>/', methods=['GET', 'DELETE'])
def retrieve_city(city_id):
    """Retrieves a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        for key, value in request_dict.items():
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
