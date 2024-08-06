#!/usr/bin/python3
"""
"places_reviews" module.
defines the Amenity view functions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_byplaceid(place_id):
    """ gets a list of all place reviews """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [r.to_dict() for r in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>/', methods=['GET'],
                 strict_slashes=False)
def get_review_byId(review_id):
    """gets a specific review using review ID"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    return abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a specific review using its ID"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a review"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        abort(400, 'Not a JSON')

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    user = storage.get(User, kwargs['user_id'])
    if not user:
        abort(404)

    if 'text' not in kwargs:
        abort(400, 'Missing text')

    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates an review"""
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for attr, val in request.get_json().items():
            if attr not in ['id', 'user_id', 'place_id',
                            'created_at', 'updated_at']:
                setattr(review, attr, val)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(404)
