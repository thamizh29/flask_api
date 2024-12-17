from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB URI with IP address of the remote MongoDB server
app.config["MONGO_URI"] = "mongodb://192.168.1.10:27017/testing"

# Initialize PyMongo
mongo = PyMongo(app)
@app.route('/')
def home():
    return render_template('new.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    # Access the collection you want to fetch data from
    collection = mongo.db.your_collection_name  # Replace with your collection name
    # Fetch all documents from the collection
    data = list(collection.find())
    # Convert MongoDB ObjectId to string for JSON compatibility
    for item in data:
        item["_id"] = str(item["_id"])  # Convert _id to string
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True,host='192.168.1.13')
