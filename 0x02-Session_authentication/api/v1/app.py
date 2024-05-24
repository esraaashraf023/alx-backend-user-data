#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.views.session_auth import *
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    auth = SessionExpAuth()
else:
    auth = Auth()

if AUTH_TYPE == "session_db_auth":
    auth = SessionDBAuth()
elif AUTH_TYPE == "session_exp_auth":
    auth = SessionExpAuth()

app.config['AUTH'] = auth
excluded_paths = ['/api/v1/status/', '/api/v1/auth_session/login/']


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request_func():
    """ Filtering of each request """
    if auth is None:
        return

    if not auth.require_auth(request.path, excluded_paths):
        return None

    if auth.authorization_header(request)\
            is None and auth.session_cookie(request) is None:
        abort(401)

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
