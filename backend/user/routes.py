from flask import Flask, jsonify, request, make_response
from app import app, db
# the above imports an instance of the flask app from app.py - this allows us to create routes.
from flask import request
from middleware.hello import Hello
from middleware.protected import Protect
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_access_cookies
from datetime import datetime, timedelta, timezone

# import the class user from our models, which we can then use in our routes.
from user.models import User




# ========= JWT as cookie approach, autho update =======
# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        print("exp_timestamp = ", exp_timestamp)
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=2))
        print("target_timestamp = ", target_timestamp)
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response



@app.route("/register", methods = ["POST", "GET"])
def signup():   
    return User().signup()

@app.route("/login", methods=["POST"])
def login():
    return User().login()


@app.route("/logout", methods=["POST"])
def logout():
    return User().logout()

# # below is a function to create the refresher token
# @app.route("/refresh", methods=["POST"])
# def refresh():
#     return Protect().refresh()

# messing around with jwt
@app.route("/unprotected")
def unprotected():
    return jsonify({
        "message" : "well done, you're in the unprotected route",
        "code" : 200
    }), 200


@app.route("/protected")
# requires a token
@jwt_required()
def protected():
    return  jsonify({"foo":"bar"})

# this gets the user:
@app.route("/user", methods=["GET"])
def get_user():
    user = Protect().get_user()
    return user["username"]

# @app.route("/get_user_data", methods=["GET"])
# def get_user():
#     user = Protect().get_user()
#     return user["username"]

@app.route("/get_user_data", methods=["GET"])
def get_user_data():
    user = User().get_user_data()
    return user

# @app.route("/get_user_by_name", methods=["GET"])
# def get_user_by_name():
    
#     user = User().get_user_by_name()
#     return user