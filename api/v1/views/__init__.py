#!/usr/bin/python3
"""
app views
defines the routes for the API
"""


from flask import Blueprint

# create app_views as instance of blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views import index, states, cities, amenities, users, places
from api.v1.views import places_reviews, places_amenities
