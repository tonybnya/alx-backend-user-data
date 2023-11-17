#!/usr/bin/env python3
"""Setting up a basic Flask app
"""
from auth import Auth
from flask import Flask, abort, jsonify, request


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def hello_world() -> str:
    """GET /
    :return: the JSON payload {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    :return: JSON payload with two forms
    - {"email": "<registered email>", "message": "user created"}
    - {"message": "email already registered"}
    """
    email, pwd = request.form.get("email"), request.form.get("password")

    try:
        AUTH.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    :return: JSON payload of the form of
    - {"email": "<user email>", "message": "logged in"}
    """
    email, pwd = request.form.get("email"), request.form.get("password")

    if not AUTH.valid_login(email, pwd):
        abort(401)

    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)

    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
