from flask_login import UserMixin
import hashlib
from flask import Flask, jsonify, request, session, redirect

import uuid

class User:
    # (UserMixin) def __init__(self, user_id, name, email, password):
    #     self.user_id = user_id
    #     self.name = name
    #     self.email = email
    #     self.password = password

    # @classmethod
    # def from_mongo(cls, user_data):
    #     return cls(
    #         user_data['_id'],
    #         user_data['name'],
    #         user_data['email'],
    #         user_data['password']
    #     )
    
    # def get_id(self):
    #     return str(self.user_id)
    
    # @classmethod
    # def get(cls, user_id):
    #     # Retrieve a user from the MongoDB database by user ID
    #     from app import db
    #     collection=db['users']
    #     user_data = collection.find_one({'_id': user_id})
    #     if user_data:
    #         return cls(user_data['_id'])
    #     return None
    
    # @staticmethod
    # def find_by_email(email):
    #     from app import db
    #     collection=db['users']
    #     user_data = collection.find_one({'email': email})
    #     if user_data:
    #         return User.from_mongo(user_data)
    #     return None

    # def save_to_mongo(self):
    #     from app import db
    #     collection=db['users']
    #     return collection.insert_one({
    #         'name': self.name,
    #         'email': self.email,
    #         'password': self.password
    #     })

        def start_session(self, user):
            del user['password']
            session['logged_in'] = True
            session['user'] = {
                'name': user['name'],  
                'email': user['email']  
            }
            return jsonify(user), 200

        def signup(self):
                from app import db1
                print(request.form)

                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                full_name = f"{first_name} {last_name}"  

                user = {
                    "_id": uuid.uuid4().hex,
                    "name": full_name,  
                    "email": request.form.get('email'),
                    "password": request.form.get('password')
                }

                # Encrypt the password using hashlib
                user['password'] = hashlib.sha256(user['password'].encode()).hexdigest()

                # Check for existing email address
                if db1.users.find_one({"email": user['email']}):
                    return jsonify({"error": "Email address already in use"}), 400

                if db1.users.insert_one(user):
                    return self.start_session(user)

                return jsonify({"error": "Signup failed"}), 400

        def signout(self):
                session.clear()
                return redirect('/')

        def login(self):
                from app import db1
                user = db1.users.find_one({
                    "email": request.form.get('email')
                })

                if user and user['password'] == hashlib.sha256(request.form.get('password').encode()).hexdigest():
                    self.start_session(user)
                    return redirect('/dashboard')
                    
                return jsonify({"error": "Invalid login credentials"}), 401
