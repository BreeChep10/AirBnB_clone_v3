#!/usr/bin/python3
"""CITY API"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", methods=[
    "GET", "POST"], strict_slashes=False)
def get_place_by_city(city_id=""):
    """GETS ALL CITIES IN A STATE"""
    result = [v for k, v in storage.all("City").
              items() if k.split(".")[1] == city_id]

    if result == []:
        abort(404)

    if request.method == "GET":
        return jsonify([place.to_dict() for place in result[0].places])

    elif request.method == "POST":
        data = request.get_json()
        if data:
            if "name" not in data:
                abort(400, "Missing name")
            if "user_id" not in data:
                abort(400, "Missing user_id")
            if len([v for k, v in storage.all("User").items() if k.
                    split(".")[1] == data["user_id"]]) == 0:
                abort(404)
            new_place = Place(city_id=city_id, **data)
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
        abort(400, "Not a JSON")


@app_views.route("/places/<place_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_place(place_id=""):
    """GETS A PLACE"""
    result = [v for k, v in storage.
              all("Place").items() if k.split(".")[1] == place_id]
    if result == []:
        abort(404)

    if request.method == "GET":
        return jsonify(result[0].to_dict())

    elif request.method == "DELETE":
        storage.delete(result[0])
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.json
        if data:
            for key, value in data.items():
                if key not in ['id', 'user_id', 'city_id', 'updated_at']:
                    setattr(result[0], key, value)
            result[0].save()
            return jsonify(result[0].to_dict()), 200
        abort(400, "Not a JSON")
