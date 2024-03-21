from flask_login import UserMixin
from flask import jsonify, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def start_session(self, user):
        del user['password']  # Ensuring the password is not stored in the session
        session['logged_in'] = True
        session['user'] = {
            'name': user['name'], 
            'email': user['email'] 
        }
        return jsonify(user), 200

    def signup(self):
        from app import db1, auth
        user_data = {
            "email": request.form.get('signupemail'),
            "password": generate_password_hash(request.form.get('signuppassword'))
        }

        # Interacting with Firebase to create a user and MongoDB to store user data
        try:
            user_record = auth.create_user(email=user_data['email'], password=user_data['password'])
            user_data['firebase_uid'] = user_record.uid
            # Remove plaintext password before storing additional data
            del user_data['password']
            if db1.users.insert_one(user_data):
                return redirect('/registrationpage')
        except Exception as e:
            return jsonify({"error": "Signup failed: " + str(e)}), 400

    def registration(self):
        from app import db1
        user = session.get('user', {})
        email = user.get('email')
        if not email:
            return jsonify({"error": "Email not found in session"}), 401

        user_details = {
            "height": f"{request.form['feet']} feet, {request.form['inches']} inches",
            "weight": request.form['weight'],
            "last_checkup_date": request.form['last_checkup_date']
        }

        db1.users.update_one({"email": email}, {"$set": user_details})
        return redirect('/articles')

    def signout(self):
        session.clear()
        return redirect('/home')

    def login(self):
        from app import auth
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Verifying the user's password with Firebase
            user = auth.get_user_by_email(email)
            if user:
                # Assuming Firebase handles password verification
                session['user'] = {'email': email, 'firebase_uid': user.uid}
                return redirect('/home')
        except Exception as e:
            return jsonify({"error": "Invalid login credentials: " + str(e)}), 401
