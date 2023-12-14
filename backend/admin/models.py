from flask import Flask, jsonify, request
from bson.json_util import dumps
from app import bcrypt, db
from bson import json_util
from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, unset_jwt_cookies

import json

class Admin:

    def sayHello(self):
        print("hello from the Admin class")
        return "hello"
    
    @jwt_required()
    def get_user_by_name(self):
        print("hello seraching time")
        name = request.args.get("name")
        results = db.users.find({"username" : {"$regex" : name, "$options" : "i"}}, {"_id": 1, "username": 1, "email" : 1, "auth_level" : 1})
        # for user in results:
        #     print(user)
        return dumps(results)
    
    @jwt_required()
    def edit_admin_user(self):
        print("updating admin user")
    
        # decode the request
        data = request.data.decode("utf-8")
        # parse JSON string
        data_json = json.loads(data)
        new_auth_level = data_json["newAuth"]
        user_to_update = data_json["userToBeEdited"]

        # find user and update
        user = db.users.find_one_and_update({"username" : user_to_update}, { "$set": { "auth_level" : new_auth_level } })

        print(user)
        
        return jsonify({
            "status": 200,
            "user": user.get("username"),
            "msg": "user authorisation has been updated"
        }), 200
    
    @jwt_required()
    def find_managers(self):
        print("looking for managers")
        
        name = request.args.get("name")

        # NOTE the use of cursor and list! This is because what we get back from the db is an iterable cursor, which we were consuming with the for loop print, thus we couldn't return it. By doing it this way we turn the cursor into a list which we can iterate over and then return. Good to know...
        
        # Find all users with username including search term, and whose auth_level is 3 or above
        results_cursor = db.users.find({
            "$and": [
                {"username" : {"$regex" : name, "$options" : "i"}},
                {"auth_level" : { "$gte": 3}}
            ]}
            , {"_id": 0, "username": 1}
            
        )
        
        results_list = list(results_cursor)
        
        # for result in results_list:
        #     print(result)
        
        return dumps(results_list)
    

    
     