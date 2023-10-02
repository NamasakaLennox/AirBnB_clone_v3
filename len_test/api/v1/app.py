#!/usr/bin/python3
"""
API endpoint to check status of app
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    obj = {"error": "Not found"}
    return (jsonify(obj), 404)

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'

    app.run(host=host, port=port, threaded=True)
