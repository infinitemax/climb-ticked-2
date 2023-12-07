from flask import Flask, jsonify, request

class Hello():

    def hi_there(self):
        print("max is cool")
        return jsonify({
            "message": "hello to you!"
        })