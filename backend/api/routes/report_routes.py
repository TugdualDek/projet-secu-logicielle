from flask import Blueprint, request, jsonify
from ...database.models.report_model import Report
from ...database.connection import DatabaseConnection

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET'])
def get_all_reports():
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        reports = db.query(Report).all()  # Récupère tous les rapports
        return jsonify([report.to_dict() for report in reports]), 200
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@reports_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        report = db.query(Report).filter_by(id=report_id).first()  # Recherche un rapport par ID
        if report is None:
            return jsonify({'error': 'Report not found'}), 404
        return jsonify(report.to_dict()), 200
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@reports_bp.route('/', methods=['POST'])
def create_report():
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        data = request.get_json()  # Récupère les données envoyées dans le body de la requête
        new_report = Report(
            scan_id=data['scan_id'],  # Crée un nouveau rapport
            findings=data['findings'],
            severity=data['severity'],
            status='generated'
        )
        db.add(new_report)  # Ajoute le rapport à la session
        db.commit()  # Valide la transaction
        return jsonify(new_report.to_dict()), 201  # Retourne le rapport créé avec un code 201
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@reports_bp.route('/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        report = db.query(Report).filter_by(id=report_id).first()  # Recherche le rapport par ID
        if report is None:
            return jsonify({'error': 'Report not found'}), 404
        
        # Mise à jour des attributs du rapport avec les données envoyées
        data = request.get_json()
        for key, value in data.items():
            setattr(report, key, value)

        db.commit()  # Valide la transaction
        return jsonify(report.to_dict()), 200  # Retourne le rapport mis à jour
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    db = DatabaseConnection.get_instance().get_session()  # Récupère la session
    try:
        report = db.query(Report).filter_by(id=report_id).first()  # Recherche le rapport par ID
        if report is None:
            return jsonify({'error': 'Report not found'}), 404

        db.delete(report)  # Supprime le rapport
        db.commit()  # Valide la transaction
        return '', 204  # Retourne un statut 204 sans contenu
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return jsonify({'error': str(e)}), 500
    finally:
        DatabaseConnection.get_instance().close_session(db)  # Ferme la session
