import json
from flask import Blueprint, request, jsonify, current_app
from ...database.models.scan_model import Scan
from ...database.connection import DatabaseConnection

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
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

    # Accéder au kernel via current_app
    kernel = current_app.kernel

    try:
        # Exécuter les workflows et récupérer les résultats
        context = {'target': target, 'scan_id': scan_id}
        final_results = kernel.execute_all_workflows(context)
    except Exception as e:
        # En cas d'erreur, mettre à jour le statut du scan en 'failed'
        db = DatabaseConnection.get_instance().get_session()
        try:
            scan = db.query(Scan).filter_by(id=scan_id).first()
            if scan:
                scan.status = 'failed'
                db.commit()
        except Exception as db_error:
            db.rollback()
            print(f"Erreur lors de la mise à jour du statut du scan : {db_error}")
        finally:
            db.close()
        return jsonify({'error': str(e)}), 500

    # Stocker les résultats du scan dans la base de données
    db = DatabaseConnection.get_instance().get_session()
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            scan.status = 'completed'
            # Convertir les résultats finaux en JSON pour les stocker
            scan.results = json.dumps(final_results)
            db.commit()
        else:
            return jsonify({'error': 'Scan not found'}), 404
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

    # Renvoyer les résultats dans la réponse de l'API
    return jsonify({
        'scan_id': scan_id,
        'results': final_results
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