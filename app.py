from flask import Flask, render_template, request,json,jsonify,send_file,session,send_from_directory,redirect, flash
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from chatgpt import callgpt_chat
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
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



# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'sugarsense',
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': 'mongodb+srv://krishnateja:Vg3cGorqg4AInMYh@sugarsense.hmv30yx.mongodb.net/?retryWrites=true&w=majority',
#             'username': 'krishnateja',
#             'password': 'Vg3cGorqg4AInMYh',
#             'authMechanism': 'SCRAM-SHA-1',
#             'authSource': 'admin'
#         }
#     }
# }

# Firebase Admin Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate('/Users/sanchay/Downloads/diabetes_umass_nursing-Sanchay_workspace/dia-user-login-firebase-adminsdk-1o8dc-00dad728ce.json')  #change path according to your system
    firebase_admin.initialize_app(cred)


app = Flask(__name__,static_folder='static')
app.secret_key = 'd21ef8b23ef23e1d5df1d7d2d037b735b0c3096fb14bcf20da5eec7e06160c33'
app.config["SESSION_TYPE"] = "filesystem"

# Set session expiration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)


def get_host_url():
    # Get the local host URL including the protocol, host, and port
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
# collection.update_many({}, { '$unset': { 'article_template': "" } })

db1 = client['User_database']
users = db1.userdata

@login_manager.user_loader
def load_user(user_id):

    return User.get(user_id)  # Implement the get method in your User model

users_collection = db.users

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
        '_id': str(article.get('_id', ''))
        # 'image': article.get('image', 'path/to/default/image.jpg'),  # Update this path to your default image
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
        print(html_template)
        update_htmlcode_of_article(ObjectId(article_id),html_template)
    return html_template


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


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = db1.users.find_one({"email": email})
    if user and sha256_crypt.verify(password, user['password']):
     
        session['user'] = user['email']  
        return redirect(url_for('dashboard'))  
    else:
        # Incorrect credentials
        flash('Invalid username/password combination')
        return redirect(url_for('loginpage'))


@app.route('/signup', methods=['POST'])
def signup():
  return User().signup()
  return jsonify({'redirect': url_for('registrationpage')})

@app.route('/registration', methods=['POST'])
def registration():
  return User().registration()


@app.route('/logout')
def logout():
    session.clear()  # Clearing all session variables
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
            except Exception as e:
                flash(f'Failed to send the password reset email. Please try again later. Error: {str(e)}', 'error')
        else:
            flash('No account found with that email address.', 'error')
        return render_template('forgot_password.html')
    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='email-reset-salt', max_age=3600)  # Verifying the token
    except SignatureExpired:
        flash('The password reset link has expired.', 'warning')  # Use 'warning' for expiration messages
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid password reset link.', 'danger')  # Use 'danger' for invalid link messages
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        if not new_password:
            flash('Password cannot be empty.', 'danger')  # Ensuring password is not empty
            return redirect(url_for('reset_password', token=token))
        
        # Here you might want to add additional checks for password strength if desired

        hashed_password = sha256_crypt.hash(new_password)
        db1.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
        flash('Your password has been successfully updated!', 'success')  # Confirming password reset success
        return redirect(url_for('loginpage'))
    return render_template('reset_password.html', token=token)



# image_download_path = '/Users/riyapalkhiwala/Desktop/Spring2024/CS682/new/diabetes_umass_nursing/link_images'
# total_images_downloaded = 0

# def get_extension_from_url(image_url):
#     if '?' in image_url:
#         image_url = image_url.split('?')[0]  # Remove query parameters
#     extension = image_url.split('/')[-1].split('.')[-1]
#     return extension

# def clean_filename(image_url):
#         # Split the filename and keep only the part before the '?'
#         filename = image_url.split('/')[-1].split('?')[0]
#         # Remove any additional extensions if present
#         parts = filename.split('.')
#         cleaned_filename = parts[0] + '.' + parts[-1]
#         return cleaned_filename


# def download_image(image_url, article_id, image_download_path):
#     # Initialize filename to None
#     filename = None

#     if image_url.startswith('data:image'):
#         match = re.search(r'base64,(.*)', image_url)
#         if match:
#             base64_data = match.group(1)
#             image_data = base64.b64decode(base64_data)
#             # Infer the extension from the MIME type in the data URL
#             extension = image_url.split(';')[0].split('/')[1]
#             filename = f"{article_id}.{extension}"
#         else:
#             print("No base64 content found in data URL.")
#             return None
#     else:
#         response = requests.get(image_url, stream=True)
#         if response.status_code == 200:
#             image_url=clean_filename(image_url)
#             extension = get_extension_from_url(image_url)
#             image_data = response.content
#             filename = f"{article_id}.{extension}"
#         else:
#             print(f"Failed to download image from {image_url}")
#             return None

#     # If a filename was set, save the image data to a file
#     if filename:
#         save_path = os.path.join(image_download_path, filename)
#         with open(save_path, 'wb') as f:
#             f.write(image_data)
#         print(f"Image saved as {filename}")
#         return filename

#     return filename


# def get_first_image_url(page_url):
#     response = requests.get(page_url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         image = soup.find('img')
#         if image and 'src' in image.attrs:
#             return image['src']
#     return None

# def update_article_image(article_id, image_filename):
#     # Update the article document in MongoDB to include the image filename
#     # result = collection.update_one({'_id': article_id}, {'$set': {'image_filename': image_filename}})
#     collection.find_one({'_id': article_id})
#     result = collection.update_one({'_id': article_id}, {'$set': {'image_filename': image_filename}})
#     if result:
#         print(f"Found  documents.")


# def download_images():
#     total_images_downloaded = 0
#     for article in collection.find():
#         link = article.get('link')
#         article_id = article.get('_id')
#         if link:
#             first_image_url = get_first_image_url(link)
#             if first_image_url:
#                 if not first_image_url.startswith(('http:', 'https:')):
#                     first_image_url = requests.compat.urljoin(link, first_image_url)
#                 image_filename = download_image(first_image_url, article_id, image_download_path)
#                 if image_filename:
#                     update_article_image(article_id, image_filename)
#                     total_images_downloaded += 1
#                     print(f"Downloaded and updated {article_id} with image {image_filename}")
#     print(f"Total images downloaded and updated in MongoDB: {total_images_downloaded}")


# def download_images_in_thread():
#     thread = threading.Thread(target=download_images)
#     thread.start()


if __name__ == '__main__':
#     # download_images_in_thread() 
     app.run(debug=True)


