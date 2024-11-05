from ..connection import DatabaseConnection

class ScanQueries:
    @staticmethod
    def create_scan(target_url):
        db = DatabaseConnection.get_instance()
        conn = db.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO scans (target_url, status, created_at)
                    VALUES (%s, %s, NOW())
                    RETURNING id, target_url, status, created_at, completed_at
                """, (target_url, 'pending'))
                conn.commit()
                return cur.fetchone()
        except Exception as e:
            conn.rollback()
            raise e

    @staticmethod
    def get_scan_by_id(scan_id):
        db = DatabaseConnection.get_instance()
        conn = db.connect()
        
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, target_url, status, created_at, completed_at
                FROM scans WHERE id = %s
            """, (scan_id,))
            return cur.fetchone()

    @staticmethod
    def update_scan_status(scan_id, status):
        db = DatabaseConnection.get_instance()
        conn = db.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE scans SET status = %s, completed_at = NOW() WHERE id = %s
                """, (status, scan_id))
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        
    @staticmethod
    def get_all_scans():
        db = DatabaseConnection.get_instance()
        conn = db.connect()

        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, target_url, status, created_at, completed_at
                FROM scans
            """)
            return cur.fetchall()
        
    @staticmethod
    def delete_scan(scan_id):
        db = DatabaseConnection.get_instance()
        conn = db.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM scans WHERE id = %s
                """, (scan_id,))
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
