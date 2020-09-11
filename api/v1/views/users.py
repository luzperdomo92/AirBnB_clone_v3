#!/usr/bin/python3
"""New view for User objects that handles all default
RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def user_index():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users_dicts = list(map(lambda user: user.to_dict(), users))
    return jsonify(users_dicts), 200


@app_views.route('/users/<user_id>', methods=['GET'])
def user_show(user_id):
    """Retrieves a User object"""
    users_found = storage.get(User, user_id)
    if users_found:
        return jsonify(users_found.to_dict()), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_destroy(user_id):
    """ Deletes a User object"""
    users_found = storage.get(User, user_id)
    if users_found:
        storage.delete(users_found)
        storage.save()
        return jsonify({}, 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'])
def user_create():
    """ Creates a User """
    user_attributes = request.get_json()
    if not user_attributes:
        abort(400, "Not a JSON")

    if 'email' not in user_attributes or not user_attributes['email']:
        abort(400, "Missing email")

    if 'password' not in user_attributes or not user_attributes['password']:
        abort(400, "Missing password")

    new_user = User(**user_attributes)
    new_user.save()

    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_update(user_id):
    users_found = storage.get(User, user_id)
    user_attributes = request.get_json()
    if not user_attributes:
        abort(400, 'Not a JSON')

    if users_found:
        for key, value in user_attributes.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(users_found, key, value)
        users_found.save()
        return(jsonify(users_found.to_dict()), 200)
    else:
        abort(404)
