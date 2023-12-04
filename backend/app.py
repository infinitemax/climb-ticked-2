from flask import Flask

app = Flask(__name__)

# Routes - this passes all the routes to our main app file
from user import routes

@app.route("/")
def home():
    return "Home"