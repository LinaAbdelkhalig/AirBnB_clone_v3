#!/usr/bin/python3
""" create the app variable, instance of Flask """


from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


# create an instance of Flask app
app = Flask(__name__)
# register the blueprint app_views to app
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(e):
    """ closes the storage """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
