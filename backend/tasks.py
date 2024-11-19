from backend.database.connection import DatabaseConnection
from backend.database.models.scan_model import Scan
from backend.core.core import Core
from backend.database.queries.reports_queries import ReportQueries
from backend.database.models.report_model import Report
import datetime
import json


def run_scan_task(scan_id):
    """
    run_scan_task Exécute un scan donné dans la queue
    :param scan_id: ID du scan
    """
    db = DatabaseConnection.get_instance().get_session()
    try:
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            scan.status = 'in_progress'
            db.commit()

            def save_results_callback(workflow_name, workflow_results):
                for result in workflow_results:
                    # Construire le nouvel enregistrement Report
                    new_report = Report(
                        scan_id=scan_id,
                        vulnerability_type=result.get('vulnerability_type', 'Unknown'),
                        vulnerability_name=result.get('vulnerability_name', 'Unknown'),
                        description=result.get('description', ''),
                        additional_info=json.dumps(result.get('additional_info', {}))
                    )
                    db.add(new_report)
                db.commit()

            core = Core()
            context = {'target': scan.target_url, 'scan_id': scan_id}
            core.execute_all_workflows(context, save_results_callback)

            scan.status = 'completed'
            scan.completed_at = datetime.datetime.now()
            db.commit()
        else:
            print(f"Scan avec l'ID {scan_id} introuvable.")
    except Exception as e:
        db.rollback()
        scan = db.query(Scan).filter_by(id=scan_id).first()
        if scan:
            scan.status = 'failed'
            db.commit()
        print(f"Erreur lors de l'exécution du scan : {e}")
    finally:
        db.close()
