from flask import Flask, request, jsonify,render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from textblob import TextBlob
import datetime

app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/aspireit'
app.config['JWT_SECRET_KEY'] = 'yb2024'

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


print("server started")

@app.route('/',methods = ['GET'])
def init():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.args
    if(request.method == 'POST') :print(request.form)
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = {'username': username, 'password': password}
    # Store user in MongoDB
    if mongo.db.users.find_one({'username': data['username']}):
        return jsonify({'message': 'choose a different username'}), 401
    mongo.db.users.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.args
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

    if request.method == 'PUT':    #testing left
        data = request.get_json()
        mongo.db.users.update_one({'username': current_user['username']}, {'$set': data})
        return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    data = request.args
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
