from flask import Flask, jsonify, request, make_response
from app import app, db
# the above imports an instance of the flask app from app.py - this allows us to create routes.
from flask import request
from middleware.hello import Hello
from middleware.protected import Protect
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_access_cookies
from datetime import datetime, timedelta, timezone

# import the class Admin from the models, which we can then use in our routes.
from admin.models import Admin
from user.models import User

@app.route("/get_user_by_name", methods=["GET"])
def get_user_by_name():
    
    user = Admin().get_user_by_name()
    return user

@app.route("/edit_admin_user_auth", methods=["POST"])
def edit_admin_user_auth():
    
    update = Admin().edit_admin_user()
    return update

@app.route("/find_managers", methods=["GET"])
def find_managers():

    results = Admin().find_managers()
    return results

