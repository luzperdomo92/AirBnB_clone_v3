#!/usr/bin/python3
"""New view for Amenity objects that handles all default
RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities_index():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenity_dicts = list(map(lambda amenity: amenity.to_dict(), amenities))
    return jsonify(amenity_dicts)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_show(amenity_id):
    """Retrieves a Amenity object"""
    amenity_found = storage.get(Amenity, amenity_id)
    if amenity_found:
        return jsonify(amenity_found.to_dict())

    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenities_destroy(amenity_id):
    """ Deletes a amenity object"""
    amenity_found = storage.get(Amenity, amenity_id)
    if amenity_found:
        storage.delete(amenity_found)
        storage.save()
        return ({}, 200)

    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities', methods=['POST'])
def amenities_create():
    """ Creates a Amenity """
    amenity_attributes = request.get_json()
    if 'name' not in amenity_attributes or not amenity_attributes['name']:
        return('Missing name', 400)

    new_amenity = Amenity(**amenity_attributes)
    new_amenity.save()

    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenities_update(amenity_id):
    amenity_found = storage.get(Amenity, amenity_id)
    amenity_attributes = request.get_json()
    if amenity_found:
        for key, value in amenity_attributes.items():
            if key != "__class__" and key != "id" and key != "created_at"\
               and key != "updated_at":
                setattr(amenity_found, key, value)
        amenity_found.save()
        return(jsonify(amenity_found.to_dict()), 200)

    return jsonify({"error": "Not found"}), 404
