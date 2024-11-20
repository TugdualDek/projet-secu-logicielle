from flask import Blueprint, request, jsonify
from ...database.models.report_model import Report
from ...database.connection import DatabaseConnection
from backend.api.utils import ErrorHandler

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET'])
def get_all_reports():
    """
    get_all_reports Récupère tous les rapports
    :return: Liste de tous les rapports
    """
    db = DatabaseConnection.get_instance().get_session()
    try:
        reports = db.query(Report).all()
        return jsonify([report.to_dict() for report in reports]), 200  
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return ErrorHandler.handle_error(e, 'Failed to retrieve reports', 500)
    finally:
        DatabaseConnection.get_instance().close_session(db)

@reports_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """
    get_report Récupère un rapport par ID
    :param report_id: ID du rapport
    :return: Détails du rapport
    """
    db = DatabaseConnection.get_instance().get_session()
    try:
        report = db.query(Report).filter_by(id=report_id).first()
        if report is None:
            return ErrorHandler.handle_error(e, 'Report not found', 404)
        return jsonify(report.to_dict()), 200
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return ErrorHandler.handle_error(e, 'Failed to retrieve report', 500)
    finally:
        DatabaseConnection.get_instance().close_session(db)

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """
    delete_report Supprime un rapport par ID
    :param report_id: ID du rapport
    :return: Statut 204 si succès
    """
    db = DatabaseConnection.get_instance().get_session()
    try:
        report = db.query(Report).filter_by(id=report_id).first()
        if report is None:
            return ErrorHandler.handle_error(e, 'Report not found', 404)

        db.delete(report)
        db.commit()
        return '', 204  # Retourne un statut 204 sans contenu
    except Exception as e:
        db.rollback()  # En cas d'erreur, rollback
        return ErrorHandler.handle_error(e, 'Failed to delete report', 500)
    finally:
        DatabaseConnection.get_instance().close_session(db)
