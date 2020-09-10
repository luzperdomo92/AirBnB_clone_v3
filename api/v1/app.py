#!/usr/bin/python3
"""Flask API for the AirBnB project"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

# Flask instance app
app = Flask(__name__)

app.url_map.strict_slashes = False
# Blueprint app_views of our Flask instance app
app.register_blueprint(app_views)

# Variables for running the Flask server
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown(self):
    """This method calls storage.close()
       after each request to the database
    """
    storage.close()


@app.errorhandler(404)
def error_404(e):
    """Returns a JSON response when error 404 occurs"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def error_400_notJson(e):
    """Returns a JSON responde when error 400 occurs"""
    return "Not a JSON", 400


if __name__ == "__main__":
    """Runs the Flask server"""
    app.run(host=host, port=port)
