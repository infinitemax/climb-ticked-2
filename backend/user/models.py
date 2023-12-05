# this is for creating our user class
from flask import Flask, jsonify, request
from app import bcrypt, db
from bson import json_util

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
                "_id" : json_util.dumps(user["_id"]),
                "username" : user["username"],
                "email" : user["email"],
                "password" : user["password"],
            }
        })