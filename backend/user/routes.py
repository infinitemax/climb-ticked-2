from flask import Flask, jsonify, request, make_response
from app import app
# the above imports an instance of the flask app from app.py - this allows us to create routes.
from flask import request
from middleware.hello import Hello
from middleware.protected import Protect
from flask_jwt_extended import jwt_required, get_jwt_identity

# import the class user from our models, which we can then use in our routes.
from user.models import User


@app.route("/register", methods = ["POST", "GET"])
def signup():
    
    return User().signup()

@app.route("/login", methods=["POST"])
def login():

    return User().login()


# messing around with jwt
@app.route("/unprotected")
def unprotected():
    return jsonify({
        "message" : "well done, you're in the unprotected route",
        "code" : 200
    }), 200


@app.route("/protected")
# requires a token

def protected():
    
    return Hello().hi_there()

# this gets the user:
@app.route("/user", methods=["GET"])
def get_user():
    user = Protect().get_user()

    return user["username"]


# below is a function to create the refresher token
@app.route("/refresh", methods=["POST"])
def refresh():
    user = Protect().refresh()
    return jsonify({
        "hello":"you",
        "user" : user
    })