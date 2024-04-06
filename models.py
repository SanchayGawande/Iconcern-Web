from flask_login import UserMixin
import hashlib
from flask import Flask, jsonify, request, session, redirect,url_for
import uuid
from passlib.hash import sha256_crypt

import logging
from datetime import datetime
class User:
    
    def start_session(self, user):

            if 'password' in user:
                del user['password']

            # Setup session
            session['logged_in'] = True
            session['user'] = {
                'email': user['email'],
                '_id': str(user['_id'])
            } 
            response_data = {
                'email': user['email'],
                '_id': str(user['_id'])
            }
            
            return jsonify(response_data), 200

    def signup(self):
                from app import db1
                user= request.json
                print(user)

                # Encrypt the password using hashlib
                user['password'] = sha256_crypt.encrypt(user['password'])

                # Check for existing email address
                if db1.users.find_one({"email": user['email']}):
                    return jsonify({"error": "Email address already in use"}), 400

                if db1.users.insert_one(user): 
                    self.start_session(user)
                    return redirect('/registrationpage')
                else:      

                    return jsonify({"error": "Signup failed"}), 400
        
    def registration(self):
                from app import db1
                user = session.get('user', {})
                email = user.get('email')
                if not email:
                    return jsonify({"error": "Email not found in session"}), 401
                
                fullName = request.form['fullName']
                age = int(request.form.get('age', 0))  # Convert age to integer
                diagnosisDate = request.form['diagnosisDate']
                bloodglucoselevels = int(request.form.get('bloodglucoselevels', 0))  # Correct variable name
                height = int(request.form.get('height', 0))
                weight = int(request.form.get('weight', 0))
                physical_activity_level = int(request.form.get('physicalactivitylevel', 0))

                # Validate age
                if age < 14 or age > 100:
                 return jsonify({"error": "Invalid age. Must be between 18 and 100."}), 400
             
                # Validate blood glucose levels
                if bloodglucoselevels < 40 or bloodglucoselevels > 600:
                 return jsonify({"error": "Blood glucose levels must be between 40 and 600."}), 400
    
                 # Validate height and weight
                if not 50 <= height <= 250 or not 20 <= weight <= 300:
                 return jsonify({"error": "Invalid height or weight."}), 400
    
                  # Validate physical activity level
                if not 1 <= physical_activity_level <= 5:
                 return jsonify({"error": "Physical activity level must be between 1 and 5."}), 400

                # Validate diagnosis date
                if datetime.strptime(diagnosisDate, '%Y-%m-%d') > datetime.now():
                 return jsonify({"error": "Diagnosis date cannot be in the future."}), 
               
                db1.users.update_one(
                    {"email": email}, 
                    {"$set": {
                        "fullName": request.form['fullName'],
                        "age": request.form['age'],
                        "gender": request.form['gender'],
                        "diagnosisDate" : request.form['diagnosisDate'],
                        "bloodglucoselevels" : request.form['bloodglucoselevels'],
                        "otherConditions" : request.form['otherConditions'],
                        "diet" :request.form['diet'],
                        "physicalactivitylevel": request.form['physicalactivitylevel'],
                        "height":request.form['height'],
                        "weight" : request.form['weight'] ,
                        "managementgoals" : request.form['managementgoals'],
                        "learningpreferences": request.form['learningpreferences'] 
                    }}
                )
                
                session.clear()
                return redirect('/loginpage')
     

    def signout(self):
                session.clear()
                return redirect('/home')

    def login(self):
            from app import db1
            email = request.form.get('email').strip()
            password = request.form.get('password')

            logging.debug(f"Login attempt for email: {email}")
            user = db1.users.find_one({"email": email})
            if user and sha256_crypt.verify(password, user['password']):
             logging.debug("Password verification succeeded.")
        # Properly initializing session
             session['user'] = user['email']
             session['logged_in'] = True
             return redirect('/home')
            else:
             logging.debug("Login failed. Email or password incorrect.")
        # It's good practice to give a generic error message
             return jsonify({"error": "Login failed. Email or password incorrect."}), 401

    def getuserprofile(self):
            from app import db1
            user = session.get('user', {})
            email = user.get('email')
            
            user_data = db1.users.find_one({
                  "email": email
                })
            
            if user_data:
                if '_id' in user_data:
                    user_data['_id'] = str(user_data['_id'])
                return jsonify(user_data)
            else:
                return jsonify({"error": "User data not found"}), 404
            
    def updateuserprofile(self):
            updated_data = request.json
            from app import db1
            user = session.get('user', {})
            email = user.get('email')

            result = db1.users.update_one({"email": email}, {"$set": updated_data})

            if result.modified_count > 0:
                return jsonify({"success": "User data updated successfully."}), 200
            else:
                return jsonify({"error": "Update failed or no changes made."}), 500
                
    def reset_password(self, email, new_password):
        # Hash the new password
            hashed_password = sha256_crypt.hash(new_password)

            from app import db1
            result = db1.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
 
            if result.modified_count == 1:
                return True  # Indicate success
            else:
                return False     
                           
            
