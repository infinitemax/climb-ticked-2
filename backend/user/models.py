# this is for creating our user class

from flask import Flask, jsonify, request
from bson.json_util import dumps
from app import bcrypt, db
from bson import json_util
from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, unset_jwt_cookies

class User:

    def signup(self):
        # each instance of a method in a class in python needs the instance of the class passed in as the first parameter, so we do this by adding "self" 

        data = request.json

        # encrypt password
        hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")


        # create user object
        #  note: auth level reflects access rights: 1 = user, 2 = setter, 3 = manager, 4 = super_admin
        user = {
            "username" : data["username"],
            "email" : data["email"],
            "password" : hashed_pw,
            "auth_level" : 1 
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

        response = jsonify({"msg": "login successful"})
        # create token
        access_token = create_access_token(identity=id)
        print("got to this point")
        set_access_cookies(response, access_token)
        return response

    @jwt_required()
    def check_auth(self):
        user_id = get_jwt_identity()
        user = db.users.find_one({"_id": ObjectId(user_id) })
        auth_level = user["auth_level"]
        
        return jsonify({"auth_level" : auth_level})

    def logout(self):
        response = jsonify({"msg" : "logout successful"})
        unset_jwt_cookies(response)
        return response

    @jwt_required()
    def get_user_data(self):
        user_id = get_jwt_identity()

        user = db.users.find_one({"_id": ObjectId(user_id) })
        print(user)

        return dumps(user)
    


    @jwt_required()
    def find_gyms(self):

        # search for gyms, return an array
        print("search term is ", request.args.get("searchTerm"))
        print("parameter is ", request.args.get("parameter"))

        searchTerm = request.args.get("searchTerm")
        parameter = request.args.get("parameter")

        gyms_cursor = db.gyms.find(
            {parameter : {"$regex" : searchTerm, "$options" : "i"}},
            {"_id" : 1, "gymName" : 1, "city" : 1, "country" : 1, "image" : 1}
        ).sort("name")

        gym_list = list(gyms_cursor)

        print(gym_list)

        for gym in gym_list:
            print(gym["gymName"])

        return dumps(gym_list)
    

   