from flask import Flask, render_template, request, jsonify, session, redirect
from functools import wraps
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# ------------------ Session ------------------
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'dev-secret'  # required for sessions
Session(app)

# ------------------ Database ------------------
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['auth_db']

users = db['users']
topics = db['topics']
comments = db['comments']

# ------------------ Auth Guard ------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# ------------------ Pages ------------------
@app.route('/login')
def login_page():
    if 'username' in session:
        return redirect('/')
    return render_template('login.html')

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

@app.route('/new-topic')
@login_required
def new_topic_page():
    return render_template('new_topic.html')

@app.route('/topic/<id>')
@login_required
def topic_page(id):
    topic = topics.find_one({'_id': ObjectId(id)})
    comment_list = list(
        comments.find({'topic_id': ObjectId(id)}).sort('created_at', 1)
    )
    return render_template('topic.html', topic=topic, comments=comment_list)

# ------------------ APIs ------------------
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return jsonify({'success': True})

    return jsonify({'success': False}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if users.find_one({'username': username}):
        return jsonify({'message': 'User exists'}), 400

    users.insert_one({
        'username': username,
        'password': generate_password_hash(password)
    })
    return jsonify({'success': True, 'message': 'Registered successfully'})

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

@app.route('/api/comments', methods=['POST'])
@login_required
def add_comment():
    data = request.json
    comments.insert_one({
        'topic_id': ObjectId(data['topic_id']),
        'body': data['body'],
        'author': session['username'],
        'created_at': datetime.utcnow()
    })
    topics.update_one(
        {'_id': ObjectId(data['topic_id'])},
        {'$inc': {'comment_count': 1}}
    )
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# ------------------ Run ------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
