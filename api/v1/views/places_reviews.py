#!/usr/bin/python3


"""Places Reviews API"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=[
    'GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    GET ALL REVIES BY PLACE
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<reviews_id>', methods=[
    'GET'], strict_slashes=False)
def get_review(review_id):
    """
    GET REVIEW BY ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=[
    'DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    DELETE REVIEW BY ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<p_id>/reviews', methods=[
    'POST'], strict_slashes=False)
def create_review(place_id):
    """
    CREATE A NEW REVIEW FOR A PLACE
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")

    new_review = Review(place_id=place_id, **data)
    storage.new(new_review)
    storage.save()

    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=[
    'PUT'], strict_slashes=False)
def update_review(review_id):
    """
    UPDATE A REVIW BY ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)

    storage.save()
