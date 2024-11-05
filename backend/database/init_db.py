import psycopg2
from ..config.settings import DATABASE_CONFIG

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = None
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG['dbname'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port']
        )
        
        # Création d'un curseur
        cur = conn.cursor()
        
        # Définition des tables
        create_tables = """
        CREATE TABLE IF NOT EXISTS scans (
            id SERIAL PRIMARY KEY,
            target_url VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS reports (
            id SERIAL PRIMARY KEY,
            scan_id INTEGER REFERENCES scans(id),
            vulnerability_type VARCHAR(100),
            severity VARCHAR(50),
            description TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # Exécution des requêtes de création
        cur.execute(create_tables)
        
        # Validation des changements
        conn.commit()
        print("Database initialized successfully!")
        
    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
        raise e
    
    finally:
        if conn:
            cur.close()
            conn.close()
