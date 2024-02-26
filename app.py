from flask import Flask, render_template, session, redirect
from functools import wraps
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = MongoClient('mongodb+srv://krishnateja:Vg3cGorqg4AInMYh@sugarsense.hmv30yx.mongodb.net/?retryWrites=true&w=majority&appName=sugarsense')
db = client['User_database']
users = db.userdata


# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')