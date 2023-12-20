from flask import Flask, jsonify, request, make_response
from app import app, db
# the above imports an instance of the flask app from app.py - this allows us to create routes.

from middleware.hello import Hello
from middleware.protected import Protect
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_access_cookies
from datetime import datetime, timedelta, timezone
import cloudinary
import cloudinary.uploader

# import the class GymAdmin from the models, which we can then use in our routes.
from gym_admin.models import GymAdmin


@app.route("/create_gym", methods=["POST"])
def create_gym():
    jwt_required()
    print("HITTING THE ADD GYM ROUTE============================================================================")
    app.logger.info("in upload route")
    # print(request.form)
    # return "hello"

    print('request.method', request.method)
    print('request.args', request.args)
    print('request.form', request.form)
    print('request.files', request.files)

    data = request.form

    # check gym doesn't already exist

    check = db.gyms.find_one({"gymName" : data["gymName"]})

    if check:
        return jsonify({
            "status" : 400,
            "message" : "this gym already exists"
        }), 400
# add message on teh front end. plus could use an npm alert package?
    upload_result = None

    # TODO - sort this so the gym is added even without an image
    if request.method == "POST":
        if "file" not in request.files:
            print("no file, how unusual")
            return "no file, how unusual"

        file_to_upload = request.files["file"]
        app.logger.info("%s file_to_upload", file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            app.logger.info(upload_result)

            url = upload_result["secure_url"]

            print("url is", url)

        elif not file_to_upload:
            url = "no image"

        # get manager ID to add to the document
        manager = db.users.find_one({ "username" : data["gymManager"]})

        print("manager is", manager)

        # create new gym object and save to db
        newGym = {
            "gymName" : data["gymName"],
            "gymManager" : data["gymManager"],
            "gymManagerId" : manager["_id"],
            "gymModerators": [],
            "gymModeratorsById": [],
            "city" : data["city"],
            "country" : data["country"],
            "image" : url,
            "cardimage" : ""
        }

        # add moderator(s)
        # iterate through list of mods in search
        # split moderators into array
        moderators = request.form["gymModerators"].split()
        
        for moderator in moderators:
            # find user by id
            new_gym_mod = db.users.find_one({"username" : moderator})
            # push username to array
            newGym["gymModerators"].append(new_gym_mod["username"])
            # push id to array
            newGym["gymModeratorsById"].append(new_gym_mod["_id"])        


        db.gyms.insert_one(newGym)

        return jsonify({
            "status": 200,
            "message": "gym successfully added, happy climbing!"
        }), 200





@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    jwt_required()
    print("=============================================================================")
    app.logger.info("in upload route")
    # print(request.form)
    # return "hello"

    print('request.method', request.method)
    print('request.args', request.args)
    print('request.form', request.form)
    print('request.files', request.files)

    upload_result = None

    if request.method == "POST":
        if "file" not in request.files:
            return "no file, how unusual"

        file_to_upload = request.files["file"]
        app.logger.info("%s file_to_upload", file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            app.logger.info(upload_result)
            return jsonify(upload_result)
        return jsonify(upload_result)

