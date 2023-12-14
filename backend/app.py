import os
from dotenv import load_dotenv
from flask import Flask

from flask_cors import CORS

from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager, get_jwt, create_access_token, set_access_cookies, get_jwt_identity

from datetime import timedelta, datetime, timezone

import pymongo

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:3000"
        }
    }, supports_credentials=True)

bcrypt = Bcrypt(app)


# configure JWT
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=6)
app.config["JWT_COOKIE_CSRF_PROTECT"] = False


jwt = JWTManager(app)


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
from admin import routes
from gym_admin import routes

# ========= JWT as cookie approach, autho update =======
# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
# NOTE - THIS USED TO BE IN THE USERS ROUTES, NOW I'VE MOVED IT HERE TO CATCH ALL ROUTES
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        print("exp_timestamp = ", exp_timestamp)
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        print("target_timestamp = ", target_timestamp)
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

@app.route("/")
def home():
    return "Home"