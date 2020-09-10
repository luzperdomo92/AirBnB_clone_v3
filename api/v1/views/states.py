#!/usr/bin/python3
"""New view for State objects that handles all default
RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def states_index():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_dicts = list(map(lambda state: state.to_dict(), states))
    return jsonify(states_dicts)


@app_views.route('/states/<state_id>', methods=['GET'])
def states_show(state_id):
    """Retrieves a State object"""
    state_found = storage.get(State, state_id)
    if state_found:
        return jsonify(state_found.to_dict())

    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'])
def states_destroy(state_id):
    """ Deletes a State object"""
    state_found = storage.get(State, state_id)
    if state_found:
        storage.delete(state_found)
        storage.save()
        return ({}, 200)

    return jsonify({"error": "Not found"}), 404


@app_views.route('/states', methods=['POST'])
def states_create():
    """ Creates a State """
    state_attributes = request.get_json()
    if 'name' not in state_attributes or not state_attributes['name']:
        return('Missing name', 400)

    new_state = State(**state_attributes)
    new_state.save()

    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def states_update(state_id):
    state_found = storage.get(State, state_id)
    state_attributes = request.get_json()
    if state_found:
        for key, value in state_attributes.items():
            if key != "__class__" and key != "id" and key != "created_at"\
               and key != "updated_at":
                setattr(state_found, key, value)
        state_found.save()
        return(jsonify(state_found.to_dict()), 200)

    return jsonify({"error": "Not found"}), 404
