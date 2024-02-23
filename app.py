from flask import Flask, render_template, request,json,jsonify,send_file,session,send_from_directory
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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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

def initialize_session():
    if 'chat_history' not in session:
        session['chat_history'] = []

@app.route('/end-session', methods=['POST'])
def end_session():
    # Ensure the session is properly initialized
    initialize_session()
    # Clear the chat history in the session to end the session
    session.pop('chat_history')
    # print(session['chat_history'] )
    return jsonify({'message': 'Session ended'})

@app.route('/save', methods=['POST'])
def save():
    HOST_URL = get_host_url()
    data = request.form.to_dict(flat=True)
    response={}
    response['author']=data['author']
    response['topic']=data['topic']
    response['description']=data['description']
    response['sub_topic_1']=data['sub_topic_1']
    response['sub_topic_1_description']=data['sub_topic_1_description']
    response["unique_url_code"]=generate_unique_urlcode()
    response["created_at"]=datetime.now()
    response["form_template"]= '<h1>working</h1>'
    inserted_id=store_form_details(response)
    if inserted_id.get("id",''):
        submit_link=HOST_URL+f'save-form-data?user_id={response["user_id"]}&form_id={inserted_id["id"]}'
        html_content=change_form_submit_url(new_url=submit_link,html_content=session['chat_history'][-1]['content'])
        hosted_link=HOST_URL+"view/{}".format(response["unique_url_code"])
        update_htmlwith_link(hosted_link,html_code=html_content,form_id=inserted_id["id"])
    end_session()
    return jsonify({'form_id':inserted_id["id"]})



########
#LOGIN#
########
@app.route('/signup', methods=['POST'])
def register():
    # Get user input from the registration form
    data = request.get_json()

    # Check if all required fields are present in the request
    required_fields = ['name', 'email', 'password', 'confirm_password']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields must be provided"}), 400

    name = data['name']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']

    # Validate user input (e.g., check for empty fields, valid email format, etc.)

    # Check if the email is already registered
    collection=db['users']
    existing_user = collection.find_one({'email': email})
    if existing_user:
        return jsonify({"error": "Email already in use. Please use a different email."}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match. Please try again."}), 400

    # Hash the user's password before storing it
    hashed_password =  sha256_crypt.using(rounds=12345).hash(password)

    # Create a new user document in MongoDB
    new_user = {
        'name': name,
        'email': email,
        'password': hashed_password
    }
    user_id = collection.insert_one(new_user).inserted_id
    # Create a User object for Flask-Login
    user = User(user_id,name,email,password)
    # Log in the user after registration
    login_user(user)
    return jsonify({"message": "Account created successfully!","user_id":user.get_id()}), 200


@app.route('/loginpage', methods=['GET'])
def loginpage():
    return render_template('loginpage.html')

@app.route('/login', methods=['POST'])
def login():
    # Get user input from the login form
    data = request.get_json()
    # Check if all required fields are present in the request
    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All required fields must be provided"}), 400

    email = data['email']
    password = data['password']

    # Check if the user exists in the database
    user = User.find_by_email(email)
    user_id = user.get_id()
    if user:
        # Verify the provided password with the hashed password in the database
        if sha256_crypt.verify(password, user.password):
            # Log in the user using Flask-Login
            login_user(user)
        
            return jsonify({"message": "Login successful",'user_id':user_id}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/logout', methods=['GET'])
# @login_required
def logout():
    # Log the user out
    logout_user()
    return 'logout'


if __name__ == '__main__':
    app.run(debug=True)
