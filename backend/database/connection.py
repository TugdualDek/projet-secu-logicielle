from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..config.settings import DATABASE_CONFIG

class DatabaseConnection:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        # Création de l'URL de connexion SQLAlchemy
        self.database_url = (
            f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
            f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"
        )
        
        # Création du moteur SQLAlchemy
        self.engine = create_engine(
            self.database_url,
            echo=False,  # Mettre à True pour voir les requêtes SQL
            pool_size=5,
            max_overflow=10,
            pool_timeout=30
        )
        
        # Création de la session factory
        session_factory = sessionmaker(bind=self.engine)
        
        # Création d'une session thread-safe
        self.Session = scoped_session(session_factory)
    
    def get_session(self):
        """Retourne une nouvelle session de base de données"""
        return self.Session()

    def close_session(self, session):
        """Ferme une session de base de données"""
        if session:
            session.close()

    def dispose(self):
        """Libère toutes les connexions du pool"""
        self.Session.remove()
        self.engine.dispose()
