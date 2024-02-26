from flask import Flask , session , redirect
from app import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
    session.clear()  # Clear the session, effectively logging the user out
    return redirect('/')  # Redirect to home page or login page
  
@app.route('/user/login', methods=['POST'])
def login():
  return User().login()