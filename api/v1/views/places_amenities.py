#!/usr/bin/python3
"""PLACE-AMENITY API"""
from os import getenv
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/amenities",
                 methods=["Get"], strict_slashes=False)
def get_amenities_of_place(place_id):
    """GETS THE AMENITIES OF A PLACE"""
    place = [v for k, v in storage.all("Place").
             items() if k.split(".")[1] == place_id]

    if place == []:
        abort(404)

    amenity = [v for k, v in storage.all("Amenity").items()]

    if request.method == "GET" and getenv("HBNB_TYPE_STORAGE") == "db":
        return jsonify([obj.to_dict() for obj in place[0].amenities])

    elif request.method == "GET":
        return jsonify([obj.to_dict() for obj in amenity if obj.
                        id in place[0].amenity_ids])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"], strict_slashes=False)
def delete_link_amenity(place_id, amenity_id):
    """DELETES OR POSTS AN AMENITY TO A PLACE"""

    place = [v for k, v in storage.all("Place").
             items() if k.split(".")[1] == place_id]

    if place == []:
        abort(404)

    amenity = [v for k, v in storage.all("Amenity").
               items() if k.split(".")[1] == amenity_id]

    if amenity == []:
        abort(404)

    if request.method == 'DELETE' and getenv(
            "HBNB_TYPE_STORAGE") == "db":
        if amenity[0] not in place[0].amenities:
            abort(404)
        place[0].amenities.remove(amenity[0])
        return jsonify({}), 200

    elif request.method == 'DELETE':
        if amenity[0].id not in place[0].amenity_ids:
            abort(404)
        place[0].amenity_ids.remove(amenity[0].id)
        return jsonify({}), 200

    if request.method == 'POST' and getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity[0] in place[0].amenities:
            return jsonify(amenity[0].to_dict()), 200
        place[0].amenities.append(amenity[0])
        storage.save()
        return jsonify(amenity[0].to_dict()), 201

    elif request.method == 'POST':
        if amenity[0].id in place[0].amenity_ids:
            return jsonify(amenity[0].to_dict()), 200
        place[0].amenity_ids.append(amenity[0].id)
        storage.save()
        return jsonify(amenity[0].to_dict()), 201
