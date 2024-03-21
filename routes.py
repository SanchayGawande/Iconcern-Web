# from flask import Flask , session , redirect
# from app import app
# from models import User


# @app.route('/signup', methods=['POST'])
# def signup():
#   return User().signup()

# @app.route('/signout')
# def signout():
#     session.clear()  # Clear the session, effectively logging the user out
#     return redirect('/dashboard')  # Redirect to home page or login page
  
# # @app.route('/login', methods=['POST'])
# # def login():
# #   return User().login()