from flask import Blueprint, request, jsonify
from ...database.models.report_model import Report
from ...database.connection import DatabaseConnection

reports_bp = Blueprint('reports', __name__)
db = DatabaseConnection.get_instance()

@reports_bp.route('/', methods=['GET'])
def get_all_reports():
    try:
        reports = db.session.query(Report).all()
        return jsonify([report.to_dict() for report in reports]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    try:
        report = db.session.query(Report).filter_by(id=report_id).first()
        if report is None:
            return jsonify({'error': 'Report not found'}), 404
        return jsonify(report.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/', methods=['POST']) 
def create_report():
    try:
        data = request.get_json()
        new_report = Report(
            scan_id=data['scan_id'],
            findings=data['findings'],
            severity=data['severity'],
            status='generated'
        )
        db.session.add(new_report)
        db.session.commit()
        return jsonify(new_report.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    try:
        report = db.session.query(Report).filter_by(id=report_id).first()
        if report is None:
            return jsonify({'error': 'Report not found'}), 404
            
        data = request.get_json()
        for key, value in data.items():
            setattr(report, key, value)
            
        db.session.commit()
        return jsonify(report.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    try:
        report = db.session.query(Report).filter_by(id=report_id).first()
        if report is None:
            return jsonify({'error': 'Report not found'}), 404
            
        db.session.delete(report)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
