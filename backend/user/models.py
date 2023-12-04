# this is for creating our user class
from flask import Flask, jsonify

class User:

    def signup(self):
        # each instance of a method in a class in python needs the instance of the class passed in as the first parameter, so we do this by adding "self" 

        user = {
            "name" : "",
            "email" : "",
            "password" : ""
        }

        return jsonify(user), 200