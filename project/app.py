from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash  # For secure passwords

app = Flask(__name__)

# MongoDB Atlas connection (use env var for security)
mongo_uri = os.environ.get('MONGO_URI')  # Set this in your environment or on Render
client = MongoClient(mongo_uri)
db = client['auth_db'] 
users = db['users']  

# Route to serve the login page (modular: add similar routes for new pages)
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

# REST API endpoint for login (POST request from JS)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful!', 'success': True})
    else:
        return jsonify({'message': 'Invalid credentials', 'success': False}), 401

# Example: Add a registration endpoint for modularity (call via JS on a register page)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if users.find_one({'username': username}):
        return jsonify({'message': 'User exists'}), 400

    hashed_pw = generate_password_hash(password)
    users.insert_one({'username': username, 'password': hashed_pw})
    return jsonify({'message': 'Registered successfully'})

#if __name__ == '__main__':
#   app.run(debug=True)  # For local dev; Render uses gunicorn
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production