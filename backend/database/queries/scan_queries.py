from ..models.report_model import Scan

class ScanQueries:
    def __init__(self, session):
        self.session = session

    def create_scan(self, target_url, status='pending'):
        scan = Scan(target_url=target_url, status=status)
        self.session.add(scan)
        self.session.commit()
        return scan

    def get_scan_by_id(self, scan_id):
        return self.session.query(Scan).filter(Scan.id == scan_id).first()
    
    def update_scan_status(self, scan_id, status):
        scan = self.get_scan_by_id(scan_id)
        if scan:
            scan.status = status
            self.session.commit()
            return scan
        return None
    
    def get_all_scans(self):
        return self.session.query(Scan).all()

    def delete_scan(self, scan_id):
        scan = self.get_scan_by_id(scan_id)
        if scan:
            self.session.delete(scan)
            self.session.commit()
            return True
        return False
