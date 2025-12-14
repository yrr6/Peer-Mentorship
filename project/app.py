from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash  # For secure passwords
from flask_session import Session
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# MongoDB Atlas connection (use env var for security)
mongo_uri = os.environ.get('MONGO_URI')  # Set this in your environment or on Render
client = MongoClient(mongo_uri)
db = client['auth_db'] 
users = db['users']
topics = db['topics']
comments = db['comments']  


from flask_session import Session  # New import
from datetime import datetime  # For timestamps
from bson.objectid import ObjectId  # For Mongo IDs

app.config['SESSION_TYPE'] = 'filesystem'  # Simple for Render
Session(app)

# Collections (add these)
topics = db['topics']
comments = db['comments']

# Update /api/login to set session
@app.route('/api/login', methods=['POST'])
def login():
    # ... (existing code)
    if user and check_password_hash(user['password'], password):
        session['username'] = username  # Set session
        return jsonify({'message': 'Login successful!', 'success': True})
    # ...

# Add logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# Middleware to protect routes (optional, but add to new-topic, etc.)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function
# Route to serve the login page (modular: add similar routes for new pages)
#@app.route('/login')
#def home():
#    if 'username' not in session:
#        return redirect('/login')  # New: Separate login route
#    topic_list = list(topics.find().sort('created_at', -1))  # Latest first
#    return render_template('home.html', topics=topic_list, username=session['username'])

@app.route('/')
@login_required
def home():
    topic_list = list(topics.find().sort('created_at', -1))
    return render_template(
        'home.html',
        topics=topic_list,
        username=session['username']
    )

@app.route('/register')
def register_page():
    return render_template('register.html')

# REST API endpoint for login (POST request from JS)
#@app.route('/api/login', methods=['POST'])
#def login():
#    data = request.json
#    username = data.get('username')
#    password = data.get('password')
#    user = users.find_one({'username': username})
#    if user and check_password_hash(user['password'], password):
#        session['username'] = username  # Set session
#        return jsonify({'message': 'Login successful!', 'success': True})
#    else:
#        return jsonify({'message': 'Invalid credentials', 'success': False}), 401
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return jsonify({'message': 'Login successful!', 'success': True})

    return jsonify({'message': 'Invalid credentials', 'success': False}), 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

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

@app.route('/new-topic', methods=['GET'])
@login_required
def new_topic_page():
    return render_template('new_topic.html')

@app.route('/api/topics', methods=['POST'])
@login_required
def create_topic():
    data = request.json
    topic = {
        'title': data['title'],
        'body': data['body'],
        'author': session['username'],
        'created_at': datetime.utcnow(),
        'comment_count': 0
    }
    result = topics.insert_one(topic)
    return jsonify({'id': str(result.inserted_id)})
@app.route('/topic/<id>')
@login_required
def topic_page(id):
    topic = topics.find_one({'_id': ObjectId(id)})
    comment_list = list(comments.find({'topic_id': ObjectId(id)}).sort('created_at', 1))
    return render_template('topic.html', topic=topic, comments=comment_list)

@app.route('/api/comments', methods=['POST'])
@login_required
def add_comment():
    data = request.json
    comment = {
        'topic_id': ObjectId(data['topic_id']),
        'body': data['body'],
        'author': session['username'],
        'created_at': datetime.utcnow()
    }
    comments.insert_one(comment)
    topics.update_one({'_id': ObjectId(data['topic_id'])}, {'$inc': {'comment_count': 1}})
    return jsonify({'message': 'Comment added'})

#if __name__ == '__main__':
#   app.run(debug=True)  # For local dev; Render uses gunicorn
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production