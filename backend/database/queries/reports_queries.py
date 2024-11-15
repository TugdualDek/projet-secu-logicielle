from backend.database.models.scan_model import Report

class ReportQueries:
    def __init__(self, session):
        self.session = session

    def create_report(self, scan_id, vulnerability_type, severity, description):
        report = Report(scan_id=scan_id, vulnerability_type=vulnerability_type, severity=severity, description=description)
        self.session.add(report)
        self.session.commit()
        return report 
    
    def get_report_by_id(self, report_id):
        return self.session.query(Report).filter(Report.id == report_id).first()
    
    def get_all_reports(self):
        return self.session.query(Report).all()
    
    def delete_report(self, report_id):
        report = self.get_report_by_id(report_id)
        if report:
            self.session.delete(report)
            self.session.commit()
            return True
        return False
