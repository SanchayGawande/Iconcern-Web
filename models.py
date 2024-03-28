from flask import Flask, jsonify, request, session, redirect,url_for
from flask_login import UserMixin
from passlib.hash import sha256_crypt
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
            if 'password' in user:
                del user['password']

            session['logged_in'] = True
            session['user'] = {
                'email': user['email']  
            }
            response_data = {
                'email': user['email']
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
                
                # height = f"{request.form['feet']} feet, {request.form['inches']} inches"
               
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
                
                email = request.form.get('email')
                password = request.form.get('password')
    
                user = db1.users.find_one({
                    "email": request.form.get('email')
                })
                # hashlib.sha256(request.form.get('password').encode()).hexdigest():
                if user and sha256_crypt.verify(password, user['password']):
                 self.start_session(user)
                 return redirect('/home')
                
                return jsonify({"error": "Invalid login credentials"}), 401
        
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
                
                
            
