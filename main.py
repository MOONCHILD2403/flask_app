from flask import Flask, request,render_template,redirect,url_for,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token,decode_token
from textblob import TextBlob
import json

with open('setup.json', 'r') as file:
    setup_data = json.load(file)

app = Flask(__name__)
app.secret_key = setup_data.get('app_secret_key')
app.config['MONGO_URI'] = setup_data.get('MONGODB_URI')
app.config['JWT_SECRET_KEY'] = setup_data.get('jwt_secret_key')

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if(request.method == 'POST'):
        data = request.form
        username = data['username']
        password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = {'username': username, 'password': password}

        if mongo.db.users.find_one({'username': data['username']}):
            return redirect(url_for('register',error = "username already in use")),301
        mongo.db.users.insert_one(user)
        return redirect(url_for('login',error = "user registered successfully")), 301
    errory = request.args.get('error') 
    return render_template('registration.html',error = errory)

@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        data = request.form
        user = mongo.db.users.find_one({'username': data['username']})
        if user and bcrypt.check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity={'username': user['username']})
            session['jwt_token'] = access_token
            return redirect(url_for('profile')),301
        return redirect(url_for('login',error = "incorrect credentials")),301
    errory = request.args.get('error')
    return render_template('login.html',error = errory)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    token = session.get("jwt_token")
    if not token:
        return redirect(url_for('login', error='access not provided')),301
    current_user = decode_token(token)['sub']
    user = mongo.db.users.find_one({'username': current_user['username']}, {'_id': 0,'password':0})
    
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':   
            data = request.form
            mydata = {}
            for k in data:
                if(k!='_method') & (data[k]!=''):
                    mydata[k] = data[k]

            if('password' in mydata):
                passwd = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                mydata['password'] = passwd
            if('username' in mydata):
                user1 = mongo.db.users.find_one({'username': mydata['username']})
                if(user1):
                   return redirect(url_for('profile',user = user, error='username already in use')),301  
                else:
                    session['jwt_token'] = create_access_token(identity={'username': mydata['username']})
            
            res = mongo.db.users.find_one_and_update({'username': user['username']}, {'$set': mydata},return_document=True )
            return redirect(url_for('profile',user = res, error='details updated successfully')),301
    errory = request.args.get('error')
    return render_template('dashboard.html',user = user,error = errory)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        data = request.form
        text = data['text']
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        analysis = {'polarity': polarity, 'subjectivity': subjectivity}
        return render_template('analyze.html',results = analysis)
    return render_template('analyze.html',results = '{msg : pls input text and submit}')

if __name__ == '__main__':
    app.run()

