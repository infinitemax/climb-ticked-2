from flask import Flask, jsonify, request, make_response
from app import app, db
# the above imports an instance of the flask app from app.py - this allows us to create routes.
from flask import request
from middleware.hello import Hello
from middleware.protected import Protect
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_access_cookies
from datetime import datetime, timedelta, timezone

# import the class GymAdmin from the models, which we can then use in our routes.
from gym_admin.models import GymAdmin


@app.route("/create_gym", methods=["POST"])
def create_gym():

    print("hitting create route")

    return "hitting create route"