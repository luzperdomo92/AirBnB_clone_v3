#!/usr/bin/python3
"""View for City objects that handles different RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_for_place(place_id, user_id):
    """Retrieves the list of all Reviews objects of a Place,
       or creates a new Review according to the request"""
    place = storage.get(Place, place_id)
    user = storage.get(User, user_id)

    if place is None or user is None:
        abort(404)

    if requested.method == 'GET':
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)

    if request.method == 'POST':
        request_dict = request.get_json()
        if not request_dict:
            abort(400, 'Not a JSON')
        if 'user_id' not in request_dict:
            abort(400, 'Missing user_id')
        if 'text' not in request_dict:
            abort(400, 'Missing text')
        new_review = Review(**request_dict)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>/', methods=['GET', 'DELETE'])
def get_or_delete(review_id):
    """Retrieves or deletes a review according to the request"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a review"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        for key, value in request_dict.items():
            if key in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
                continue
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
