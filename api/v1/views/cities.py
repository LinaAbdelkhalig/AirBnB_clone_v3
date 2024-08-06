#!/usr/bin/python3
"""
"cities" module.
defines the City view functions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_bystate(state_id):
    """ gets a list of all cities in a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city_byId(city_id):
    """gets a specific city using city ID"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a specific city using its ID"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a state"""
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for attr, val in request.get_json().items():
            if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, attr, val)
        city.save()
        return jsonify(city.to_dict()), 200
    abort(404)
