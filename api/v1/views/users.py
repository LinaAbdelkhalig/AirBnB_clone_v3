#!/usr/bin/python3
"""
"users" module.
defines the User view functions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ gets a list of all users """
    u_items = storage.all(User).items()
    users = [val.to_dict() for attr, val in u_items]
    return jsonify(users)


@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
def get_user_byId(user_id):
    """gets a specific user using user ID"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a specific user using its ID"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'email' not in kwargs:
        abort(400, 'Missing email')
    if 'password' not in kwargs:
        abort(400, 'Missing password')
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates an user"""
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for attr, val in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(user, attr, val)
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404)
