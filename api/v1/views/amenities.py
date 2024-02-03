#!/usr/bin/python3
"""STATES API"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
def amenities_fetch():
    """GETS ALL AMENITIES"""
    if request.method == 'POST':
        data = request.get_json()
        if data is not None:
            if 'name' not in data:
                abort(400, "Missing name")
            new = Amenity(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201
        abort(400, "Not  a JSON")
    elif request.method == "GET":
        amenities = storage.all("Amenity").values()
        return jsonify([obj.to_dict() for obj in amenities])


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def amenities_by_id(amenity_id=""):
    """GETS AN AMENITY  BY ID AND OR DELETES IT OR UPDATES IT"""
    result = [v for k, v in storage.all("Amenity").
              items() if k.split(".")[1] == amenity_id]
    if result == []:
        abort(404)
    if request.method == "DELETE":
        storage.delete(result[0])
        storage.save()
        return jsonify({}), 200
    elif request.method == 'GET':
        return jsonify(result[0].to_dict())
    elif request.method == "PUT":
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(result[0], key, value)
            result[0].save()
            return jsonify(result[0].to_dict()), 200
        abort(400, "Not a  JSON")
