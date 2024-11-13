import json
from flask import Blueprint, request, jsonify, current_app
from ...database.models.scan_model import Scan
from ...database.connection import DatabaseConnection
from ...config.settings import REDIS_CONFIG
from backend.tasks import run_scan_task
from rq import Queue
from redis import Redis

# Créez une connexion Redis et initialisez la queue
redis_conn = Redis(host=REDIS_CONFIG['HOST'], port=REDIS_CONFIG['PORT'])
q = Queue('scan_tasks', connection=redis_conn)

scans_bp = Blueprint('scans', __name__)

# Route pour récupérer tous les scans
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


# Route pour récupérer un scan par ID
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

# Route pour démarrer un scan
@scans_bp.route('/', methods=['POST'])
def start_scan():
    data = request.get_json()
    target = data.get('target')

    # Valider les données
    if not target:
        return jsonify({'error': 'Missing parameter "target"'}), 400

    # Créer une entrée de scan en base de données
    db = DatabaseConnection.get_instance().get_session()
    try:
        new_scan = Scan(target_url=target, status='pending')
        db.add(new_scan)
        db.commit()
        scan_id = new_scan.id
        scan_status = new_scan.status
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

    # Ajouter la tâche à la queue RQ
    q.enqueue(run_scan_task, scan_id)

    # Renvoyer les résultats dans la réponse de l'API
    return jsonify({
        'scan_id': scan_id,
        'status': scan_status,
    }), 200

# Route pour supprimer un scan par ID
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

# Route pour récupérer les résultats d'un scan par ID
@scans_bp.route('/<int:scan_id>/results', methods=['GET'])
def get_scan_results(scan_id):
    db = DatabaseConnection.get_instance().get_session()
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            return jsonify({
                'scan_id': scan.id,
                'status': scan.status,
                'results': json.loads(scan.results) if scan.results else None
            }), 200
        else:
            return jsonify({'error': 'Scan not found'}), 404
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@scans_bp.route('/<int:scan_id>/status', methods=['GET'])
def get_scan_status(scan_id):
    db = DatabaseConnection.get_instance().get_session()
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            return jsonify({
                'scan_id': scan.id,
                'status': scan.status
            }), 200
        else:
            return jsonify({'error': 'Scan not found'}), 404
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()