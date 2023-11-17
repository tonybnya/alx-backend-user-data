#!/usr/bin/env python3
"""Setting up a basic Flask app
"""
from auth import Auth
from flask import Flask, abort, jsonify, redirect, request


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def hello_world() -> str:
    """GET /
    :return: the JSON payload {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> None:
    """DELETE /sessions
    :return: nothing and redirect to home route '/'
    """
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)

    if user_cookie is None and user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    :return: JSON payload of the form of
    - {"email": "<user email>"}
    """
    user_cookie = request.cookies.get("session_id", None)

    if user_cookie is None:
        abort(403)

    user = AUTH.get_user_from_session_id(user_cookie)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    :return: JSON payload of the form of
    - {"email": "<user email>", "reset_token": "<reset token>"}
    """
    try:
        email = request.form["email"]
    except KeyError:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    :return: JSON payload of the form of
    - {"email": "<user email>", "message": "Password updated"}
    """
    try:
        email = request.form["email"]
        reset_token = request.form["reset_token"]
        new_password = request.form["new_password"]
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
