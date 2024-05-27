from flask import Flask, request, jsonify,render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from textblob import TextBlob
import re

app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/aspireit'
app.config['JWT_SECRET_KEY'] = 'yb2024'

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# @app.before_request
# def before_request():
#     # Check if the content type is JSON
#     if request.content_type == 'application/json':
#         print("jsno dtype")
#         try:
#             request.json_data = request.get_json()
#         except Exception as e:
#             request.json_data = None
#     # Check if the content type is form-encoded
#     elif request.content_type == 'application/x-www-form-urlencoded':
#         request.json_data = request.form.to_dict()
#     else:
#         request.json_data = None

# @app.route('/')
# def home():
#     return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    
    data = request.form
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = {'username': username, 'password': password}

    if mongo.db.users.find_one({'username': data['username']}):
        return jsonify({'message': 'choose a different username'}), 401
    mongo.db.users.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    user = mongo.db.users.find_one({'username': data['username']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity={'username': user['username']})
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    if request.method == 'GET':
        user = mongo.db.users.find_one({'username': current_user['username']}, {'_id': 0, 'password': 0})
        return jsonify(user), 200

    if request.method == 'PUT':    
        data = request.form
        mydata = {k:v for k,v in data.items()}
        if('password' in data):
            passwd = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            mydata['password'] = passwd
        if('username' in data):
            user = mongo.db.users.find_one({'username': data['username']})
            if(user):
                return jsonify({'message':'user with a same name already exists please choose  different name'}),401

        mongo.db.users.update_one({'username': current_user['username']}, {'$set': mydata})
        return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    data = request.form
    text = data['text']
    analysis = TextBlob(text).sentiment
    return jsonify({'polarity': analysis.polarity, 'subjectivity': analysis.subjectivity}), 200

# # Security measures
# @app.before_request
# def before_request():
#     # Input validation and security checks
#    pass

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

