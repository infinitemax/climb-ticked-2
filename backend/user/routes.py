from flask import Flask
from app import app
# the above imports an instance of the flask app from app.py - this allows us to create routes.

# import the class user from our models, which we can then use in our routes.
from user.models import User

@app.route("/user/signup", methods = ["GET"])
def signup():
    return User().signup()