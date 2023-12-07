# this is for creating our user class
from flask import Flask, jsonify, request
from app import bcrypt, db
from bson import json_util
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token

class User:

    def signup(self):
        # each instance of a method in a class in python needs the instance of the class passed in as the first parameter, so we do this by adding "self" 

        data = request.json

        # encrypt password
        hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")


        # create user object
        user = {
            "username" : data["username"],
            "email" : data["email"],
            "password" : hashed_pw,
            "is_admin" : False
        }

        # check for existing usernames
        check = db.users.find_one({"username" : user["username"]})

        if check:
            return jsonify({
                "status" : 400,
                "message" : "username already taken"
            }), 400
        
        # check for existing emails
        check = db.users.find_one({"email" : user["email"]})

        if check:
            return jsonify({
                "status" : 400,
                "message" : "email already registered"
            }), 400

        db.users.insert_one(user)

        print(user)
        return jsonify({
            "status" : 200,
            "message": "success",
            "user" : {
                # TODO sort this out!
                "_id" : json_util.dumps(user["_id"]),
                "username" : user["username"],
                "email" : user["email"],
                "password" : user["password"],
            }
        })
    

    def login(self):
        # get data
        data = request.json.get
        username = data("username")
        password = data("password")

        # check for inputs
        if not username:
            return jsonify({
                "message" : "Please provide a username"
            }), 400
        
        if not password:
            return jsonify({
                "message" : "Please provide a password"
            }), 400

        # check for user
        user = db.users.find_one({"username" : username})

        if not user:
            return jsonify({
                "message" : "No user of that name - (case sensitive)"
            }), 400

        # verify password
        valid_password = bcrypt.check_password_hash(user["password"], password)

        if not valid_password:
            return jsonify({
                "message" : "Incorrect password"
            }), 400

        # ========create token========
        # get user ID
        id = str(user["_id"])
        access_token = create_access_token(identity=id)
        refresh_token = create_refresh_token(identity=id)



        print(username, password)
        return jsonify(
            {"message" : "success",
             "valid_pw" : valid_password,
             "access_token" : access_token,
             "refresh_token" : refresh_token,
             "id" : id}
            ), 200