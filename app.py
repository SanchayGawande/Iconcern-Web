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
cred = credentials.Certificate('/Users/sanchay/Downloads/CS682 - project/diabetes_umass_nursing-Sanchay_workspace/diabetes_umass_nursing-Riya_workspace/dia-user-login-firebase-adminsdk-1o8dc-00dad728ce.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__,static_folder='static')
app.secret_key = 'd21ef8b23ef23e1d5df1d7d2d037b735b0c3096fb14bcf20da5eec7e06160c33'
def get_host_url():
    # Get the local host URL including the protocol, host, and port
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

    return User.get(user_id)  # Implement the get method in your User model



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
  return User().login()

@app.route('/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/register-user', methods=['POST'])
def register_user():
    user_data = request.json
    if not user_data:
        return jsonify({'error': 'No user data provided'}), 400
    users_collection = db1['users']  
    try:
        # Insert user data into the 'users' collection
        users_collection.insert_one(user_data)
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/registration', methods=['POST'])
def registration():
  return User().registration()

@app.route('/verify-email')
def verify_email():
    return render_template('verify_email.html')


@app.route('/logout')
def signout():
    return User().signout()



if __name__ == '__main__':
    app.run(debug=True)
