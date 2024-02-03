#!/usr/bin/python3
"""USER API"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
def users_fetch():
    """GETS ALL USERS"""
    if request.method == 'POST':
        data = request.get_json()
        if data is not None:
            if 'email' not in data:
                abort(400, "Missing email")
            if 'password' not in data:
                abort(400, "Missing password")
            new = User(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201
        abort(400, "Not  a JSON")
    elif request.method == "GET":
        users = storage.all("User").values()
        return jsonify([obj.to_dict() for obj in users])


@app_views.route("/users/<user_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def users_by_id(user_id=""):
    """GETS USERS  BY ID AND OR DELETES IT OR UPDATES IT"""
    result = [v for k, v in storage.all("User").
              items() if k.split(".")[1] == user_id]
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
