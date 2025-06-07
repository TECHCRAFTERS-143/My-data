from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Invalid input"}), 400

    existing_user = mongo.db.users.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "❌ Username already exists!"}), 409

    mongo.db.users.insert_one({"username": username, "password": password})
    return jsonify({"message": "✅ User registered successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
