from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Routes - this passes all the routes to our main app file
from user import routes

@app.route("/")
def home():
    return "Home"