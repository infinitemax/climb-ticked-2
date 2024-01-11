from flask import Flask, jsonify, request, make_response
from app import app, db
# the above imports an instance of the flask app from app.py - this allows us to create routes.


from middleware.protected import Protect
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_access_cookies
from datetime import datetime, timedelta, timezone

from gyms.models import Gym

@app.route("/gyms/<id>", methods=["GET"])
def find_gym(id):

    return Gym().find_gym(id)