#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.city import City
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=[
    "GET", "POST"], strict_slashes=False)
def get_cities_by_state(state_id=""):
    """GETS ALL CITIES IN A STATE"""
    result = [v for k, v in storage.all("State").
              items() if k.split(".")[1] == state_id]

    if result == []:
        abort(404)

    if request.method == "GET":
        return jsonify([city.to_dict() for city in result[0].cities])

    elif request.method == "POST":
        data = request.get_json()
        if data:
            if "name" not in data:
                abort(400, "Missing name")
            new_city = City(state_id=state_id, **data)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
        abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_city(city_id):
    """GETS A CITY"""
    result = [v for k, v in storage.
              all("City").items() if k.split(".")[1] == city_id]
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
                if key not in ['id', 'state_id', 'updated_at']:
                    setattr(result[0], key, value)
            result[0].save()
            return jsonify(result[0].to_dict()), 200
        abort(400, "Not a JSON")
