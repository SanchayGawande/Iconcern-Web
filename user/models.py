import hashlib
from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
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
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and user['password'] == hashlib.sha256(request.form.get('password').encode()).hexdigest():
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401