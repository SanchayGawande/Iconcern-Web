from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    @classmethod
    def from_mongo(cls, user_data):
        return cls(
            user_data['_id'],
            user_data['name'],
            user_data['email'],
            user_data['password']
        )
    
    def get_id(self):
        return str(self.user_id)
    
    @classmethod
    def get(cls, user_id):
        # Retrieve a user from the MongoDB database by user ID
        from app import db
        collection=db['users']
        user_data = collection.find_one({'_id': user_id})
        if user_data:
            return cls(user_data['_id'])
        return None
    
    @staticmethod
    def find_by_email(email):
        from app import db
        collection=db['users']
        user_data = collection.find_one({'email': email})
        if user_data:
            return User.from_mongo(user_data)
        return None

    def save_to_mongo(self):
        from app import db
        collection=db['users']
        return collection.insert_one({
            'name': self.name,
            'email': self.email,
            'password': self.password
        })


