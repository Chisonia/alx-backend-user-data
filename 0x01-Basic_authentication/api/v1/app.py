#!/usr/bin/env python3
"""API entry point."""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth  # Import the BasicAuth class

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app)

auth = None
auth_type = getenv("AUTH_TYPE")  # Get the AUTH_TYPE environment variable

# Use BasicAuth if AUTH_TYPE is set to 'basic_auth', else fall back to Auth
if auth_type == "basic_auth":
    auth = BasicAuth()  # Create an instance of BasicAuth
elif auth_type == "auth":
    auth = Auth()  # Fallback to Auth


@app.before_request
def before_request():
    """Filter requests before processing."""
    if auth is None:
        print("Auth is None")
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']  # noqa: E501
    if not auth.require_auth(request.path, excluded_paths):
        print(f"Request to {request.path} does not require auth")
        return
    if auth.authorization_header(request) is None:
        print(f"Authorization header missing for {request.path}")
        abort(401)
    if auth.current_user(request) is None:
        print(f"User not found for {request.path}")
        abort(403)


@app.errorhandler(401)
def unauthorized(error):
    """Handles 401 error."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handles 403 error."""
    return jsonify({"error": "Forbidden"}), 403


@app.route('/api/v1/status', methods=['GET'])
def status():
    """Returns the API status."""
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
