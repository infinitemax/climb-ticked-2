from flask import Flask, jsonify, request
from bson.json_util import dumps
from app import bcrypt, db
from bson import json_util
from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, unset_jwt_cookies

class Admin:

    def sayHello(self):
        print("hello from the Admin class")
        return "hello"
    
    @jwt_required()
    def get_user_by_name(self):
        name = request.args.get("name")
        user = db.users.find_one({"username" : name})
        print(user)
        return dumps(user)