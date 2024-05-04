from flask import Flask, render_template, request,json,jsonify,send_file,session,send_from_directory,redirect
from chatgpt import callgpt_chat
#from form_parser import change_form_submit_url
from article_to_html import json_to_html
from pymongo import MongoClient
from bson import ObjectId
import urllib
from datetime import datetime
from flask_cors import CORS
from passlib.hash import sha256_crypt
from flask_login import LoginManager,login_user,login_required,logout_user
from bs4 import BeautifulSoup
from models import User
from functools import wraps
import pandas as pd
import firebase_admin
from firebase_admin import credentials, auth
from datetime import timedelta
from PIL import Image
import io
import os
import subprocess
import threading
import requests
import re
import base64
from bson import SON
from flask import Flask, render_template, request,json,jsonify,send_file,session,send_from_directory,redirect, redirect, url_for, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from article_to_html import json_to_html
from pymongo import MongoClient
from bson import ObjectId
import urllib
import pymongo
from datetime import datetime
from flask_cors import CORS
from passlib.hash import sha256_crypt
from flask_login import LoginManager,login_user,login_required,logout_user
from bs4 import BeautifulSoup
from models import User
from functools import wraps
import pandas as pd
import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask
from flask_cors import CORS

if not firebase_admin._apps:

    cred = credentials.Certificate('/Users/sanchay/Downloads/CromeDownloads/diabetes_umass_nursing_integrated/dia-user-login-firebase-adminsdk-1o8dc-00dad728ce.json')
    firebase_admin.initialize_app(cred)

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__,static_folder='static')
def get_host_url():

    local_host_url = request.host_url
    return local_host_url 

# Configure your Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Correct port for SSL
app.config['MAIL_USE_TLS'] = False  # TLS should be False when using SSL
app.config['MAIL_USE_SSL'] = True  # SSL is enabled
app.config['MAIL_USERNAME'] = 'iconcern01@gmail.com'
app.config['MAIL_PASSWORD'] = 'qiklxtldyqqepbax'  # Use an app password if 2FA is enabled
app.config['MAIL_DEFAULT_SENDER'] = 'iconcern01@gmail.com'


mail = Mail(app)

app.secret_key = 'd21ef8b23ef23e1d5df1d7d2d037b735b0c3096fb14bcf20da5eec7e06160c33'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
app.config["SESSION_TYPE"] = "filesystem"

# Set session expiration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)


def get_host_url():
    local_host_url = request.host_url
    return local_host_url 


# CORS(app,origins=[HOST_URL])

username = "krishnateja"
password = "Vg3cGorqg4AInMYh"
cluster_name = "sugarsense.hmv30yx"
database_name = "sugarsense"

# Escape username and password using urllib.parse.quote_plus
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# MongoDB Atlas connection URI
mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_name}.mongodb.net/{database_name}?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)  # Change the URL to your MongoDB server URL
db = client["sugarsense"]  # Change 'mydatabase' to your database name
collection=db["articles_articles"]
login_manager = LoginManager(app)

db1 = client['User_database']
users = db1.userdata

@login_manager.user_loader
def load_user(user_id):

    return User.get(user_id)  



@app.route('/check')
def check_mongodb_connection():
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        # Attempt to run a simple command
        db_stats = client.admin.command('ping')
        return jsonify({"message": "MongoDB Connection is successful!", "status": db_stats})
    except Exception as e:
        return jsonify({"message": "MongoDB Connection Failed", "error": str(e)}), 500
    
@app.route('/dashboard/allvalues')
def articledetails():
    data = collection.find()
    
    # Convert MongoDB cursor to a list of dictionaries
    data_list = [json.loads(json.dumps(item,default=str)) for item in data]
    
    # Return the data as JSON response
    return jsonify(data_list), 200

    # except Exception as e:
    #         return jsonify({"error": str(e)}), 500

@app.route('/getallcategories')
def getallcategories():

    pipeline = [
    {"$unwind": "$category"},
    {"$group": {"_id": "$category"}},
    
    ]
    unique_categories = collection.aggregate(pipeline)
    categories_list = [cat['_id'] for cat in unique_categories]
    return jsonify(categories_list),200
    
@app.route('/dashboard/form-details/', methods=['POST'])
#example for inserting collection should be replaced wth form
def store_form_details(data):
    try:
        result = collection.insert_one(data)
        return {"message": "Data inserted successfully", "id": str(result.inserted_id)}
    except Exception as e:
       return jsonify({"error": str(e)})


@app.route('/dashboard/article-details/all/<article_id>', methods=['GET'])
def get_form_details_all(article_id):
    #try:
    query={'id':article_id}
    #print(query)
    # Query the collection to retrieve data (modify as needed)
    data = collection.find(query)
    #print(data)
    # Convert MongoDB cursor to a list of dictionaries
    data_list = [json.loads(json.dumps(item,default=str)) for item in data]
    # Return the data as JSON response
    #print(data_list)
    return jsonify(data_list), 200

    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500



@app.route('/dashboard/form-details/<string:id>', methods=['DELETE'])
def delete_form_details(id):
    inserted_id=''
    return inserted_id

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/home')
def dashboard():
    return render_template('home.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/search_articles', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    query = {
        "$or": [
            {"topic": {"$regex": keyword, "$options": "i"}},
            {"decription": {"$regex": keyword, "$options": "i"}},
            {"sub_topic_1": {"$regex": keyword, "$options": "i"}},
            {"sub_topic_2": {"$regex": keyword, "$options": "i"}},
            {"sub_topic_3": {"$regex": keyword, "$options": "i"}}
        ]
    } if keyword else {}
    total_count = collection.count_documents(query)
    results = collection.find(query).skip((page - 1) * limit).limit(limit)
    
    articles = [{
        'topic': article.get('topic', 'No Title'),#change made here as in my article card it was not able to get title
        
        'author': article.get('author', 'No Author'),
        '_id': str(article.get('_id', '')),
        'image_filename': article.get('image_filename',''),  # Update this path to your default image
        # Add any other fields you need
    } for article in results]

    return jsonify({
        'articles': articles,
        'total_count': total_count,
        'total_pages': (total_count + limit - 1) // limit,
    })

@app.route('/dashboard/form-response')
def form_response():
    return render_template('formresponse.html')

@app.route('/download', methods=['GET'])
def download_file():
    # Specify the file path (replace with your file's actual path)
    file_path_js = 'form_data.json'
    file_path_csv = 'form_data.csv'
    with open(file_path_js) as f:
        data = [json.loads(line) for line in f]

    # Converting JSON data to a pandas DataFrame
    df = pd.DataFrame(data)
    df.to_csv("form_data.csv", index=False)
    # Define the file name as seen by the client (you can change this)
    file_name = 'form_response.csv'

    try:
        # Send the file as a response
        return send_file(file_path_csv, as_attachment=True, download_name=file_name)
    except FileNotFoundError:
        return "File not found", 404


import uuid

def generate_unique_urlcode(length=7):
    return str(uuid.uuid1())[:length]

@app.route('/generate/magiclink',methods=['POST'])
def generate_user_url():
    data = request.form.to_dict(flat=True)
    HOST_URL = get_host_url()
    query={'user_id':ObjectId(data['user_id']),'_id':ObjectId(data['form_id'])}
    uid = db.form.find(query,{'magic_link':1,'unique_url_code':1,'_id':0})

    #json.loads(json.dumps(item,default=str))
    data_list = [item for item in uid]
    print(data_list)
    if data_list:
        if data_list[0].get('magic_link',None):
            return jsonify({'sharablelink':data_list[0]['magic_link']})
        elif data_list[0].get('unique_url_code',None):
            return jsonify({'sharablelink':HOST_URL+"view/{}".format(data_list[0]['unique_url_code'])}),200
    else:
        return jsonify({"message": "URL not generated please retry check if given params exist"}), 404


def update_htmlcode_of_article(article_id,html_code):
    try:
        query={
            "_id":ObjectId(article_id)
        }
        #print("HELLO",query)
        update_fields={
            "$set":{"article_template":html_code}
        }
        # Update document
        result = collection.update_one(query, update_fields)
        if result.matched_count == 1 and result.modified_count == 1:
            return jsonify({"message": "Document updated successfully"}), 200
        else:
            return jsonify({"message": "Document not found or not updated"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def chat():
    data = request.form.to_dict(flat=True)
    response=json_to_html(data)
    return render_template('index.html',content=response)

@app.route('/view/<article_id>',methods=['GET'])
def view_user_article(article_id):
    query={'_id':ObjectId(article_id)}
    html_template=collection.find_one(query,{'article_template':1,'_id':0}) # The params in this response are form_template,_id 
    #print('html_TEMP:',html_template)
    if html_template:
        html_template = BeautifulSoup(html_template.get('article_template','<h1>No article available</h1>'),features="html.parser")
        html_template = html_template.prettify()
    else:
        query={'_id':ObjectId(article_id)}
        article_data=collection.find_one(query,{'_id':0})
        html_template = BeautifulSoup(json_to_html(article_data), 'html')
        html_template = html_template.prettify()
        update_htmlcode_of_article(ObjectId(article_id),html_template)
    return render_template('article_display.html', article_html=html_template)

    #return html_template

# @app.route('/getcategory/<category>', methods=['GET'])
# def get_category_articles(category):



########
#LOGIN#
########
# Decorators


# Authentication decorator to verify Firebase ID token
def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        id_token = request.headers.get('Authorization')
        if not id_token:
            return jsonify({"error": "Authorization token not provided"}), 401
        try:
            decoded_token = auth.verify_id_token(id_token)
            request.user = decoded_token
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return wrapper

@app.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')

@app.route('/registrationpage')
def registrationpage():
    return render_template('registration.html')

# @app.route('/articles')
# def articles():
#     return render_template('articles.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = db1.users.find_one({"email": email})
    if user and sha256_crypt.verify(password, user['password']):
        session['user'] = user['email']  # Store user email in session
        return redirect(url_for('articles'))
    else:
        flash('Invalid username/password combination')
        return redirect(url_for('loginpage'))

import logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.get_json()
    user_data['password'] = sha256_crypt.hash(user_data['password'])
    if db1.users.find_one({"email": user_data['email']}):
        return jsonify({"error": "Email address already in use"}), 400

    if db1.users.insert_one(user_data).inserted_id:
        session['email'] = user_data['email']
        print("Session set:", session)  # Debug: Check what's in the session
        return redirect(url_for('registrationpage'))
    else:
        return jsonify({"error": "Signup failed"}), 400




@app.route('/registration', methods=['POST'])
def registration():
    if 'email' not in session:
        return jsonify({'error': 'Session not found. Please log in.'}), 400

    email = session['email']
    user_data = request.form.to_dict()  # Assuming data is sent as form data

    # Debugging: Print or log the data received to ensure it's correct
    app.logger.debug("Registration data received: %s", user_data)

    # Ensure all fields are present
    required_fields = ['fullName', 'age', 'gender', 'streetAddress', 'city', 'state', 'zipCode', 'country', 'diagnosisDate', 'fastingGlucose', 'hba1c', 'medications', 'otherConditions', 'diet', 'physicalactivitylevel', 'weight', 'height', 'managementgoals', 'learningpreferences']
    if not all(field in user_data for field in required_fields):
        return jsonify({'error': 'Missing one or more required fields.'}), 400

    # Update the user profile in MongoDB
    try:
        result = db1.users.update_one(
            {'email': email},
            {'$set': user_data}
        )
        if result.modified_count == 1:
            return redirect(url_for('articles'))
        else:
            return jsonify({'error': 'No updates made to the profile.'}), 404
    except Exception as e:
        app.logger.error("Failed to update user profile: %s", str(e))
        return jsonify({'error': 'Failed to update due to an error.'}), 500
    
    
@app.route('/social_registration', methods=['POST'])
def social_registration():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Session not initialized correctly.'}), 400

    user_data = request.form.to_dict()

    # Validation of user data, example: checking age
    if int(user_data.get('age', 0)) < 18:
        return jsonify({'error': 'Age must be at least 18.'}), 400

    # Update user data in MongoDB
    update_result = db1.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_data},
        upsert=False  # Ensure no new documents are created
    )

    if update_result.modified_count > 0:
        return redirect(url_for('articles'))
    else:
        return jsonify({'error': 'Failed to update user data.'}), 400


    

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove 'user' from session
    return redirect(url_for('loginpage'))

@app.route('/userprofile', methods=['GET'])
def userprofile():
    return render_template('UserProfile.html')

@app.route('/getuserprofile')
def get_user_profile():
   return User().getuserprofile()

@app.route('/updateuserprofile', methods=['POST'])
def update_user_profile():
    return User().updateuserprofile()


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        user = db1.users.find_one({"email": email})
        if user:
            try:
                token = serializer.dumps(email, salt='email-reset-salt')
                reset_url = url_for('reset_password', token=token, _external=True)
                msg = Message("Password Reset Request", recipients=[email])
                msg.body = f"Please click on the link to reset your password: {reset_url}"
                mail.send(msg)
                flash('Please check your email for a password reset link.', 'info')
                app.logger.info(f"Password reset email sent successfully to {email}")
            except Exception as e:
                app.logger.error(f"Failed to send email: {e}")
                flash('Failed to send the password reset email. Please try again later.', 'error')
                return render_template('forgot_password.html')
            return redirect(url_for('loginpage'))
        else:
            flash('No account found with that email address.', 'error')
    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = None
    try:
        email = serializer.loads(token, salt='email-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('The password reset link has expired.', 'danger')
        app.logger.warning("Expired token for password reset.")
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid password reset link.', 'danger')
        app.logger.error("Invalid token for password reset.")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        hashed_password = sha256_crypt.hash(new_password)
        db1.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
        flash('Your password has been updated!', 'success')
        app.logger.info(f"Password updated for {email}")
        return redirect(url_for('loginpage'))
    
    return render_template('reset_password.html', token=token)


@app.route('/signup/facebook', methods=['POST'])
def facebook_signup():
    data = request.get_json()
    if not data or 'firebase_token' not in data:
        return jsonify({'error': 'No data provided'}), 400

    firebase_token = data['firebase_token']
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        user_info = auth.get_user(decoded_token['uid'])

        # Check if the user already exists
        existing_user = db1.users.find_one({"firebase_uid": user_info.uid})
        if existing_user:
            # If user exists, update session and redirect
            session['user_id'] = str(existing_user['_id'])
            return jsonify({'redirect': url_for('dashboard')})
        else:
            # Create new user if not exists
            new_user_data = {
                "email": user_info.email,
                "displayName": user_info.display_name,
                "firebase_uid": user_info.uid,
                "photoUrl": user_info.photo_url
            }
            result = db1.users.insert_one(new_user_data)
            session['user_id'] = str(result.inserted_id)
            return jsonify({'redirect': url_for('registrationpage')})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/login/facebook', methods=['POST'])
def facebook_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    firebase_token = data.get('firebase_token')
    if not firebase_token:
        return jsonify({'error': 'Firebase token is missing'}), 400

    try:
        decoded_token = auth.verify_id_token(firebase_token)
        uid = decoded_token['uid']
        existing_user = db1.users.find_one({"firebase_uid": uid})
        if existing_user:
            session['user'] = str(existing_user['_id'])
            return jsonify({'redirect_url': url_for('dashboard'), 'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'User does not exist, please sign up.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/signup/google', methods=['POST'])
def google_signup():
    data = request.get_json()
    if not data or 'firebase_token' not in data:
        return jsonify({'error': 'Firebase token not provided'}), 400

    firebase_token = data['firebase_token']
    try:
        # Verify the ID token while checking if the token is revoked by passing check_revoked=True.
        decoded_token = auth.verify_id_token(firebase_token, check_revoked=True)
        uid = decoded_token['uid']

        # Check if user exists in your DB or create a new one
        existing_user = db1.users.find_one({"firebase_uid": uid})
        if not existing_user:
            user_data = {
                "email": decoded_token['email'],
                "displayName": decoded_token.get('name', ''),
                "firebase_uid": uid,
                "photoUrl": decoded_token.get('picture', '')
            }
            db1.users.insert_one(user_data)
            session['user_id'] = str(user_data['_id'])
            # Redirect to registration page to complete the profile
            return jsonify({'redirect_url': url_for('registrationpage')})
        else:
            session['user_id'] = str(existing_user['_id'])
            # Redirect to dashboard if user already exists
            return jsonify({'redirect_url': url_for('dashboard')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/login/google', methods=['POST'])
def google_login():
    data = request.get_json()
    if not data or 'firebase_token' not in data:
        return jsonify({'error': 'Firebase token not provided'}), 400

    firebase_token = data['firebase_token']
    try:
        # Verify the ID token while checking if the token is revoked by passing check_revoked=True.
        decoded_token = auth.verify_id_token(firebase_token, check_revoked=True)
        uid = decoded_token['uid']

        # Check if user exists in your DB or create a new one
        existing_user = db1.users.find_one({"firebase_uid": uid})
        if existing_user:
            session['user_id'] = str(existing_user['_id'])
            # Redirect to dashboard if user already exists
            return jsonify({'redirect_url': url_for('dashboard')})
        else:
            return jsonify({'error': 'User does not exist, please sign up.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/categorizedarticle',methods=['GET'])
def categorizedarticle():
    return render_template('categorizedarticle.html')


@app.route('/getarticles/<category>', methods=['GET'])
def get_category_articles(category):
    try:
        # Using $in to check if the category list includes the given category
        articles = collection.find({"category": {"$in": [category]}})
        articles_list = [json.loads(json.dumps(article, default=str)) for article in articles]
        return jsonify(articles_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# function to start chatbotdef start_chainlit():
def start_chainlit():
    # Assuming 'Llama2_chatbot' is in the current directory or adjust the path as necessary
    # chatbot_dir = os.path.join(os.path.dirname(__file__), 'Llama2_chatbot')
    command = ["chainlit", "run", "model.py"]
    subprocess.Popen(command)

def run_chainlit_in_thread():
    thread = threading.Thread(target=start_chainlit)
    thread.start()


# if __name__ == '__main__':
# #     # download_images_in_thread() 
#     run_chainlit_in_thread()
#     app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run(debug=True) 
