#!/usr/bin/python3
"""New view for Amenity objects that handles all default
RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities_index():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenity_dicts = list(map(lambda amenity: amenity.to_dict(), amenities))
    return jsonify(amenity_dicts), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_show(amenity_id):
    """Retrieves a Amenity object"""
    amenities_found = storage.get("Amenity", amenity_id)
    if amenities_found:
        return jsonify(amenities_found.to_dict()), 200
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenities_destroy(amenity_id):
    """ Deletes a amenity object"""
    amenities_found = storage.get("Amenity", amenity_id)
    if amenities_found:
        storage.delete(amenities_found)
        storage.save()
        return ({}, 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'])
def amenities_create():
    """ Creates a Amenity """
    amenity_attributes = request.get_json()
    if not amenity_attributes:
        abort(400, "Not a JSON")

    if 'name' not in amenity_attributes or not amenity_attributes['name']:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity_attributes)
    new_amenity.save()

    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenities_update(amenity_id):
    amenities_found = storage.get("Amenity", amenity_id)
    amenity_attributes = request.get_json()
    if not amenity_attributes:
        abort(400, "Not a JSON")

    if amenities_found:
        for key, value in amenity_attributes.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenities_found, key, value)
        storage.save()
        return(jsonify(amenities_found.to_dict()), 200)
    else:
        abort(404)
