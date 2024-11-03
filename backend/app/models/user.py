#Définit les modèles de données (utilisateurs, comptes, transactions).
# Importation des bibliotheques
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import config
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.get_default_database()

class User :
    def __init__(self, first_name, last_name, email, password, password_hash=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash or generate_password_hash(password)


    def save(self):
        usr_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password_hash
        }
        db.users.insert_one(usr_data)

    @staticmethod
    def find_by_email(email):
        user_data = db.users.find_one({'email': email})
        if user_data:
            return User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password="",
                password_hash=user_data['password']
            )
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)










