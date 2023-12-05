import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import pymongo

load_dotenv()

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

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