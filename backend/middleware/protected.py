from flask import Flask, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app import db
from bson import ObjectId

class Protect():
    
    # decorator that requires a refresh token
    @jwt_required(refresh=True)
    def refresh(self):
    # grabs the payload from the jwt, which we add to var user_id
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        return jsonify({
            "msg": user_id,
            "access_token" : access_token
        })
    
    @jwt_required()
    def get_user(self):
        user_id = ObjectId(get_jwt_identity())
    
        user = db.users.find_one({"_id" : user_id})

        del user["_id"]

        return jsonify(user)