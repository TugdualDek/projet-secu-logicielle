from flask import Blueprint, request, jsonify
from ...database.models.scan_model import Scan
from ...database.connection import DatabaseConnection

scans_bp = Blueprint('scans', __name__)

@scans_bp.route('/', methods=['GET'])
def get_all_scans():
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        scans = db.query(Scan).all()  # Récupère tous les scans
        return jsonify([scan.to_dict() for scan in scans]), 200
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@scans_bp.route('/<int:scan_id>', methods=['GET']) 
def get_scan(scan_id):
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()  # Recherche un scan par ID
        if scan is None:
            return jsonify({'error': 'Scan not found'}), 404
        return jsonify(scan.to_dict()), 200
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@scans_bp.route('/', methods=['POST'])
def create_scan():
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        data = request.get_json()  # Récupère les données envoyées dans le body de la requête
        new_scan = Scan(
            target_url=data['target_url'],  # Crée un nouveau scan
            status='pending'
        )
        db.add(new_scan)  # Ajoute le scan à la session
        db.commit()  # Valide la transaction
        return jsonify(new_scan.to_dict()), 201  # Retourne le scan créé avec un code 201
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@scans_bp.route('/<int:scan_id>', methods=['PUT'])
def update_scan(scan_id):
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()  # Recherche le scan par ID
        if scan is None:
            return jsonify({'error': 'Scan not found'}), 404
        
        # Mise à jour des attributs du scan avec les données envoyées
        data = request.get_json()
        for key, value in data.items():
            setattr(scan, key, value)

        db.commit()  # Valide la transaction
        return jsonify(scan.to_dict()), 200  # Retourne le scan mis à jour
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@scans_bp.route('/<int:scan_id>', methods=['DELETE'])
def delete_scan(scan_id):
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()  # Recherche le scan par ID
        if scan is None:
            return jsonify({'error': 'Scan not found'}), 404

        db.delete(scan)  # Supprime le scan
        db.commit()  # Valide la transaction
        return '', 204  # Retourne un statut 204 sans contenu
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session