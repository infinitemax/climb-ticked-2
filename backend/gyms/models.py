import json
from flask import Flask, jsonify, request
from bson.json_util import dumps
from app import bcrypt, db
from bson import json_util
from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, unset_jwt_cookies


class Gym:

    def find_gym(self, gym_id):

        gym = db.gyms.find_one({"_id" : ObjectId(gym_id)})
        gym["stringId"] = gym_id
        print(gym)
        return json.loads(json_util.dumps(gym))