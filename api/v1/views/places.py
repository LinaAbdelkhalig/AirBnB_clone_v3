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
from models.user import User


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


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
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
def create_place(city_id):
    """creates a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')

    user = storage.get(User, kwargs['user_id'])
    if not user:
        abort(404)
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates an place"""
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for attr, val in request.get_json().items():
            if attr not in ['id', 'user_id', 'city_id',
                            'created_at', 'updated_at']:
                setattr(place, attr, val)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for places based on the JSON in the request body"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = [p.to_dict() for p in storage.all(Place).values()]
    else:
        places = []

        # Add places for each state
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        if place.to_dict() not in places:
                            places.append(place.to_dict())

        # Add places for each city
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place.to_dict() not in places:
                        places.append(place.to_dict())

        # Filter places by amenities
        if amenities:
            places = [p for p in places if
                      all(a in p['amenities'] for a in amenities)]

    return jsonify(places)
