#!/usr/bin/python3
"""CITY API"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import jsonify, abort, request
from os import getenv


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


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def place_search():
    """Search for places based on given criteria"""
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    states_ids = data.get("states", [])
    cities_ids = data.get("cities", [])
    amenity_ids = data.get("amenities", [])

    all_cities = []
    all_places = []

    if not states_ids and not cities_ids:
        all_places = [v for k, v in storage.all("Place").items()]
    else:
        for id in states_ids:
            state = storage.get("State", id)
            if state:
                all_cities += [city for city in state.cities]
        for id in cities_ids:
            city = storage.get("City", id)
            if city and city not in all_cities:
                all_cities.append(city)

        for item in all_cities:
            all_places += item.places

    filtered_places = []
    for place in all_places:
        if amenity_ids:
            if getenv("HBNB_TYPE_STORAGE") == 'db':
                place_amenity_ids = [amenity.id for amenity in place.amenities]
            else:
                place_amenity_ids = place.amenity_ids
            if all([amenity_id in place_amenity_ids
                    for amenity_id in amenity_ids]):
                filtered_places.append(place)
        else:
            filtered_places.append(place)
    return jsonify([obj.to_dict() for obj in filtered_places])
