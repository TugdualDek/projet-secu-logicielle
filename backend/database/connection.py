import psycopg2
from ..config.settings import DATABASE_CONFIG

class DatabaseConnection:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=DATABASE_CONFIG['dbname'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                host=DATABASE_CONFIG['host'],
                port=DATABASE_CONFIG['port']
            )
            return self.conn
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
