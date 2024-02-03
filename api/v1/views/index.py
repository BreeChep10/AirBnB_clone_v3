#!/usr/bin/python3
"""index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns server status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """RETURNS THE OBJECTS STATS COUNT"""
    result = {
        'amenities': storage.count("Amenity"),
        'cities': storage.count("City"),
        'places': storage.count("Place"),
        'reviews': storage.count("Review"),
        'states': storage.count("State"),
        'users': storage.count("User")
    }

    return jsonify(result)
