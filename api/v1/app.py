#!/usr/bin/python3
"""FLASK APP"""


from os import getenv
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(cmd):
    """CLOSES CURRENT SESSION"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """HANDLES PAGE NOT FOUND(404)"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True)
