from flask import Blueprint, request, jsonify
from ...database.models.scan_model import Scan
from ...database.connection import DatabaseConnection

scans_bp = Blueprint('scans', __name__)
db = DatabaseConnection.get_instance()

@scans_bp.route('/', methods=['GET'])
def get_all_scans():
    try:
        scans = db.session.query(Scan).all()
        return jsonify([scan.to_dict() for scan in scans]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scans_bp.route('/<int:scan_id>', methods=['GET']) 
def get_scan(scan_id):
    try:
        scan = db.session.query(Scan).filter_by(id=scan_id).first()
        if scan is None:
            return jsonify({'error': 'Scan not found'}), 404
        return jsonify(scan.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scans_bp.route('/', methods=['POST'])
def create_scan():
    try:
        data = request.get_json()
        new_scan = Scan(
            target=data['target'],
            scan_type=data['scan_type'],
            status='pending'
        )
        db.session.add(new_scan)
        db.session.commit()
        return jsonify(new_scan.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@scans_bp.route('/<int:scan_id>', methods=['PUT'])
def update_scan(scan_id):
    try:
        scan = db.session.query(Scan).filter_by(id=scan_id).first()
        if scan is None:
            return jsonify({'error': 'Scan not found'}), 404
            
        data = request.get_json()
        for key, value in data.items():
            setattr(scan, key, value)
            
        db.session.commit()
        return jsonify(scan.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@scans_bp.route('/<int:scan_id>', methods=['DELETE'])
def delete_scan(scan_id):
    try:
        scan = db.session.query(Scan).filter_by(id=scan_id).first()
        if scan is None:
            return jsonify({'error': 'Scan not found'}), 404
            
        db.session.delete(scan)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
