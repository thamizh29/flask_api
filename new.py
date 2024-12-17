from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://192.168.1.10:27017/testing"
mongo = PyMongo(app)

# Route: Render HTML Page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route: Add New User to MongoDB
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.json
#     name = data.get('name')
#     age = data.get('age')
#     hobbies = data.get('hobbies')

#     # Store in MongoDB
#     users_collection = mongo.db.users
#     users_collection.insert_one({
#         "name": name,
#         "age": age,
#         "hobbies": hobbies
#     })

#     return jsonify({"message": "User added successfully"}), 200

# Route: Fetch Users
@app.route('/get_users', methods=['GET'])
def get_users():
    users_collection = mongo.db.users
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users), 200

if __name__ == "_main_":
    app.run(debug=True)