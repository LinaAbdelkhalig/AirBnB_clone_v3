#!/usr/bin/python3
"""
"places" module.
defines the Place view functions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.state import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_bycity(city_id):
    """ gets a list of all places """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [p.to_dict() for p in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>/', methods=['GET'], strict_slashes=False)
def get_place_byId(place_id):
    """gets a specific place using place ID"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a specific place using its ID"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place():
    """creates a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates an place"""
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for attr, val in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(place, attr, val)
        place.save()
        return jsonify(place.to_dict()), 200
    abort(404)
