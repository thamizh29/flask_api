from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection URI
mongo_uri = "mongodb://192.168.1.10:27017/testing"
client = MongoClient(mongo_uri)

# Access the 'testing' database and 'users' collection
db = client['testing']
users_collection = db['users']

# API endpoint to fetch all users
@app.route('/get_users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(users)

# API endpoint to add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if data:
        users_collection.insert_one(data)
        return jsonify({"message": "User added successfully!"}), 201
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)