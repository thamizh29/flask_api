from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/auth_db"
mongo = PyMongo(app)

# Secret key for JWT (use a secure random value in production)
SECRET_KEY = "58e2b02dc130d44d2dcd4f9ffefe0667992afc5decdff51d5402a6e2ab9a0565"

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
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

    return {"status": "success", "message": "User registered successfully"}, 200
@app.route('/view', methods=['GET'])
def view():
    users_collection = mongo.db.users
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(users)

@app.route('/login', methods=['POST'])
def login():
    users_collection = mongo.db.users
    login_data = request.get_json()

    # Validate input data
    if not login_data or 'email' not in login_data or 'password' not in login_data:
        return {"status": "error", "message": "Invalid input data"}, 400

    # Fetch the user from the database
    user = users_collection.find_one({"email": login_data['email']})
    if not user:
        return {"status": "error", "message": "User not found"}, 404

    # Verify the password
    if not check_password_hash(user['password'], login_data['password']):
        return {"status": "error", "message": "Invalid password"}, 401

    # Generate JWT token
    payload = {
        "email": user['email'],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"status": "success", "token": token}, 200
@app.route('/forget',methods=['POST'])
def forget():
    return

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
