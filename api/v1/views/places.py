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


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def place_search():
    """A PLACE SEARCH"""
    all_cities = []

    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    states_ids = data.get("states")
    cities_ids = data.get("cities")
    amenity_ids = data.get("amenities")

    if not states_ids and not cities_ids:
        all = [v for k, v in storage.all("Place").items()]
        if amenity_ids and getenv('HBNB_STORAGE_TYPE') == 'db':
            for item in all:
                item_amenities = [obj.id for obj in item.amenities]
                for i in amenity_ids:
                    if i not in item_amenities:
                        all.remove(item)
                        break
            return jsonify([obj.to_dict() for obj in all])
        elif amenity_ids:
            for item in all:
                for i in amenity_ids:
                    if i not in item.amenity_ids:
                        all.remove(item)
                        break
            return jsonify([obj.to_dict() for obj in all])
        else:
            return jsonify([obj.to_dict() for obj in all])

    if states_ids and states_ids != []:
        states = [v for k, v in storage.all("State").
                  items() if k.split(".")[1] in states_ids]
        for obj in states:
            for item in obj.cities:
                all_cities.append(item)

    if cities_ids and cities_ids != []:
        cities = [v for k, v in storage.all("City").
                  items() if k.split(".")[1] in cities_ids]
        for obj in cities:
            if obj not in all_cities:
                all_cities.append(obj)

    all_places = [x for y in all_cities for x in y.places]

    if amenity_ids and getenv("HBNB_STORAGE_TYPE") == 'db':
        for k, item in enumerate(all_places):
            item_amenity_id = [x.id for x in item.amenities]
            for i in amenity_ids:
                if i not in item_amenity_id:
                    del all_places[k]
                    break
        return jsonify([item.to_dict() for item in all_places])
    elif amenity_ids:
        for k, item in enumerate(all_places):
            for i in amenity_ids:
                if i not in item.amenity_ids:
                    del all_places[k]
                    break
        return jsonify([obj.to_dict() for obj in all_places])
    else:
        return jsonify([obj.to_dict() for obj in all_places])
