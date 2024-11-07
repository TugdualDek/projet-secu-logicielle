import os

DATABASE_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'vulnerability_scanner'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432),
    'database_initialized': False
}

API_CONFIG = {
    'HOST': os.getenv('HOST', 'localhost'),
    'PORT': os.getenv('PORT', 5000),
    'DEBUG': os.getenv('DEBUG', True)
}