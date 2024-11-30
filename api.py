from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

# Initialize the Flask application
app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_account"  # Use your MongoDB URI here
mongo = PyMongo(app)

@app.route('/')
def home():
    return "Welcome to the Flask MongoDB App!"

# Route to fetch data from MongoDB
@app.route('/get_data')
def get_data():
    # Access the 'users' collection
    users_collection = mongo.db.users
    # Fetch all users from the collection
    users = users_collection.find()
    # Convert the users data to a list and return as JSON
    users_list = [{'name': user['name'], 'email': user['email']} for user in users]
    return jsonify(users_list)

@app.route('/create_data', methods=['POST'])
def create_data():
   
    collection = mongo.db.users  # This is the 'users' collection within 'myDatabase'
    
    # Get the data from the POST request (JSON data)
    user_data = request.get_json()
    
    # Insert the data into the collection
    collection.insert_one(user_data)

    return jsonify({"message": "Data inserted successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
