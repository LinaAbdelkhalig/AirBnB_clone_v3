#!/usr/bin/python3
""" app views """


from flask import Blueprint


# create app_views as instance of blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
