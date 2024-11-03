#Contient les configurations de l'application (clés secrètes, URI de la base de données, etc.).
# Moduls importation.
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'feDr4oCZJU98O7FyTs4dpZI9+eHTDcQz'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/FortiCheck_DB'
