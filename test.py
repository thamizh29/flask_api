from flask import Flask , jsonify, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://192.168.1.10:27017/testing"
mongo = PyMongo(app)

client = MongoClient(app.config["MONGO_URI"])
db = client.testing  # Select the "testing" database

@app.route('/')
def signup_temp():
    return render_template('signup.html')

@app.route('/users', methods=['POST'])
def add_user():
    """Add a new user to the 'users' collection."""
    name = request.form.get('username')  # Fetch 'username' from form data
    password = request.form.get('password')  # Fetch 'password' from form data

    if not name or not password:
        return jsonify({"error": "Invalid data"}), 400

    mongo.db.users.insert_one({
        "username": name,
        "password": password
    })
    return jsonify({"message": "User added successfully"}), 201

@app.route('/signup', methods=['POST'])
def Login():
    users_collection = mongo.db.users
    user_data = request.get_json()

    # Validate input data
    if not user_data or 'email' not in user_data or 'password' not in user_data:
        return {"status": "error", "message": "Invalid input data"}, 400

    # Check if the user already exists
    if users_collection.find_one({"email": user_data['email']}):
        return {"status": "error", "message": "User already exists"}, 409

    # Hash the password before storing it
    hashed_password = generate_password_hash(user_data['password'])

    # Insert the new user into the database
    users_collection.insert_one({
        "email": user_data['email'],
        "password": hashed_password,
        "created_at": datetime.datetime.utcnow()
    })

    return {"status": "success", "message": "User registered successfully"}, 201

@app.route('/data', methods=['GET'])
def get_users():
    """Fetch all users from the 'users' collection."""
    users = mongo.db.users.find({}, {"_id": 0})  # Exclude the ObjectId from the results
    return jsonify(list(users))

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='192.168.1.13', port=5000 ,debug=True)
