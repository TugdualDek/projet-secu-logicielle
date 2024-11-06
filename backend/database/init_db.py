from sqlalchemy import inspect
from .models.base import Base
from .models.scan_model import Scan
from .models.report_model import Report
from .connection import DatabaseConnection

def check_tables_exist():
    """Check if all required tables exist"""
    db = DatabaseConnection.get_instance()
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())
    required_tables = {'scans', 'reports'}
    return required_tables.issubset(existing_tables)

def init_database():
    """Initialize the database and create tables if they don't exist"""
    if check_tables_exist():
        print("Database tables already exist!")
        return False
        
    try:
        db = DatabaseConnection.get_instance()
        Base.metadata.create_all(db.engine)
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e
