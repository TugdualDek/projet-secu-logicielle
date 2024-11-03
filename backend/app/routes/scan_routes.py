from flask import Blueprint, request, jsonify
from ..models.scan import Scan
from attack_modules.auth.bruteforce import BruteforceScanner

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/start', methods=['POST'])
def start_scan():
    data = request.json
    target = data.get('target')
    scan_type = data.get('scan_type')

    if not target:
        return jsonify({'error': 'Target URL is required'}), 400

    if scan_type not in ['bruteforce']:  # Ajouter d'autres types plus tard
        return jsonify({'error': 'Invalid scan type'}), 400

    try:
        # Créer et exécuter le scanner approprié
        if scan_type == 'bruteforce':
            scanner = BruteforceScanner(target)
            results = scanner.scan()

            # Sauvegarder les résultats
            scan = Scan(
                target=target,
                scan_type=scan_type,
                results=results
            )
            scan.save()

            return jsonify({
                'message': 'Scan completed',
                'results': results
            }), 200

    except Exception as e:
        return jsonify({
            'error': f'Scan failed: {str(e)}'
        }), 500

@scan_bp.route('/status/<scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    scan = Scan.find_by_id(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404

    return jsonify({
        'status': scan.status,
        'results': scan.results
    }), 200