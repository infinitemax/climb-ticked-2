import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
import pymongo

load_dotenv()

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# configure JWT
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)

SECRET_KEY = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY

# Database
# Add this dotenv stuff when I know the db is working.
MONGODB_URI = os.getenv("MONGODB_URI")
app.config["MONGO_URI"] = MONGODB_URI


client = pymongo.MongoClient(MONGODB_URI)
db = client.users

# Routes - this passes all the routes to our main app file
from user import routes

@app.route("/")
def home():
    return "Home"