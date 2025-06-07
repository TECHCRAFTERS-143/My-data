from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder=".")
CORS(app)

# MongoDB Atlas URL from environment variable or direct string (for local test)
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://<user>:<pass>@cluster.mongodb.net/db")
client = MongoClient(MONGO_URI)
db = client["signupdb"]
collection = db["users"]

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if collection.find_one({"username": username}):
        return jsonify({"message": "Username already exists!"})
    collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "User registered successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
