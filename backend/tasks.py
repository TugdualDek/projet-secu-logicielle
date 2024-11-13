from backend.database.connection import DatabaseConnection
from backend.database.models.scan_model import Scan
from backend.core.core import Kernel
import json

def run_scan_task(scan_id):
    db = DatabaseConnection.get_instance().get_session()
    try:
        # Mettre à jour le statut du scan à "in_progress"
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            scan.status = 'in_progress'
            db.commit()

            # Exécuter le scan
            kernel = Kernel()
            context = {'target': scan.target_url, 'scan_id': scan_id}
            final_results = kernel.execute_all_workflows(context)

            # Mettre à jour le statut du scan à "completed" et stocker les résultats
            scan.status = 'completed'
            scan.results = json.dumps(final_results)
            db.commit()
        else:
            print(f"Scan avec l'ID {scan_id} introuvable.")
    except Exception as e:
        db.rollback()
        # Mettre à jour le statut du scan à "failed"
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            scan.status = 'failed'
            db.commit()
        print(f"Erreur lors de l'exécution du scan : {e}")
    finally:
        db.close()