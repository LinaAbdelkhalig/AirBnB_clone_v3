#!/usr/bin/python3
"""
"amenities" module.
defines the Amenity view functions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.state import State


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities_bystate():
    """ gets a list of all amenities """
    a_items = storage.all(Amenity).items()
    amenities = [val.to_dict() for attr, val in a_items]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
def get_amenity_byId(amenity_id):
    """gets a specific amenity using amenity ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a specific amenity using its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a amenity"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    amenity = Amenity(**kwargs)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity"""
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for attr, val in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, attr, val)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
