#!/usr/bin/python3
""" create the app variable, instance of Flask """


from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


# create an instance of Flask app
app = Flask(__name__)
# set up the cors
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# register the blueprint app_views to app
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(e):
    """ closes the storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handles the 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
