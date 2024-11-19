import json
from flask import Blueprint, request, jsonify, current_app
from backend.database.models.scan_model import Scan
from backend.database.connection import DatabaseConnection
from backend.config.settings import REDIS_CONFIG
from backend.tasks import run_scan_task
from backend.api.utils import ErrorHandler
from rq import Queue
from redis import Redis

# Créez une connexion Redis et initialisez la queue
redis_conn = Redis(host=REDIS_CONFIG['HOST'], port=REDIS_CONFIG['PORT'])
q = Queue('scan_tasks', connection=redis_conn)

scans_bp = Blueprint('scans', __name__)

@scans_bp.route('/', methods=['GET'])
def get_all_scans():
    """
    get_all_scans Récupère tous les scans
    :return: Liste de scans
    """
    db = DatabaseConnection.get_instance().get_session()
    try:
        scans = db.query(Scan).all()  # Récupère tous les scans
        return jsonify([scan.to_dict() for scan in scans]), 200
    except Exception as e:
        db.rollback() 
        return ErrorHandler.handle_error(e, 'Failed to retrieve scans', 500)
    finally:
        DatabaseConnection.get_instance().close_session(db)


@scans_bp.route('/<int:scan_id>', methods=['GET']) 
def get_scan(scan_id):
    """
    get_scan Récupère un scan par ID
    :param scan_id: ID du scan
    :return: Détails du scan
    """
    db = DatabaseConnection.get_instance().get_session() 
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first() 
        if scan is None:
            return ErrorHandler.handle_error(None, 'Scan not found', 404)
        return jsonify(scan.to_dict()), 200
    except Exception as e:
        db.rollback()
        return ErrorHandler.handle_error(e, 'Failed to retrieve scan', 500)
    finally:
        DatabaseConnection.get_instance().close_session(db)

@scans_bp.route('/', methods=['POST'])
def start_scan():
    """
    start_scan Démarre un scan
    :return: ID du scan et statut
    """
    data = request.get_json()
    target = data.get('target')

    # Valider les données
    if not target:
        return ErrorHandler.handle_error(None, 'Missing parameter "target"', 400)

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
        return ErrorHandler.handle_error(e, 'Failed to start scan', 500)
    finally:
        db.close()

    # Ajouter la tâche à la queue RQ
    q.enqueue(run_scan_task, scan_id)

    return jsonify({
        'scan_id': scan_id,
        'status': scan_status,
    }), 200

@scans_bp.route('/<int:scan_id>', methods=['DELETE'])
def delete_scan(scan_id):
    """
    delete_scan Supprime un scan par ID
    :param scan_id: ID du scan
    :return: Réponse vide
    """
    db = DatabaseConnection.get_instance().get_session()
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan is None:
            return ErrorHandler.handle_error(None, 'Scan not found', 404)

        db.delete(scan)
        db.commit()
        return '', 204
    except Exception as e:
        db.rollback() 
        return ErrorHandler.handle_error(e, 'Failed to delete scan', 500)
    finally:
        DatabaseConnection.get_instance().close_session(db)

@scans_bp.route('/<int:scan_id>/status', methods=['GET'])
def get_scan_status(scan_id):
    """
    get_scan_status Récupère le statut d'un scan par ID
    :param scan_id: ID du scan
    :return: Statut du scan
    """
    db = DatabaseConnection.get_instance().get_session()
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            return jsonify({
                'scan_id': scan.id,
                'status': scan.status
            }), 200
        else:
            return ErrorHandler.handle_error(None, 'Scan not found', 404)
    except Exception as e:
        db.rollback()
        return ErrorHandler.handle_error(e, 'Failed to retrieve scan status', 500)
    finally:
        db.close()