#Gère les routes d'authentification (connexion, inscription).
# Importations des bibliotheques

# routes/auth_routes.py
from flask import Blueprint, request, session, jsonify
from ..models.user import User

auth_bp = Blueprint('auth', __name__)
# Route d'inscription
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Utiliser .get() correctement avec une valeur par défaut
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    email = data.get('email', '')
    password = data.get('password', '')

    # Vérifier que tous les champs requis sont présents et non vides
    if not all([first_name, last_name, email, password]):
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    # Vérifier si l'utilisateur existe déjà
    if User.find_by_email(email):
        return jsonify({'error': 'Un utilisateur avec cet email existe déjà'}), 409

    try:
        # Créer et sauvegarder le nouvel utilisateur
        new_user = User(first_name, last_name, email, password)
        new_user.save()

        # Créer la session
        session['email'] = email

        return jsonify({
            'message': 'Inscription réussie',
            'user': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        }), 201

    except Exception as e:
        return jsonify({'error': f'Erreur lors de l\'inscription: {str(e)}'}), 500

# Route de connexion
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    #récupérer les données de connexion
    email = data.get('email', '')
    password = data.get('password', '')

    # vérifier que tous les champs sont remplis
    if not all([email, password]):
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    #Rechercher l'utilisateur
    user = User.find_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({'error': 'Email ou password incorrect'}), 401

    #Crée la session
    session['email'] = email

    #renvoyer les infos de l'utilisateur
    return jsonify({
        'message': 'Connexion réussie',
        'user':{
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
    }), 200

# gestion du logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return jsonify({'message':'Déconnexion réussie'}), 200








































