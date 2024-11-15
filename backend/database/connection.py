from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.config.settings import DATABASE_CONFIG

class DatabaseConnection:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """
        get_instance Récupère une instance de la connexion à la base de données
        :return: Instance de la connexion à la base de données
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        # Création de l'URL de connexion SQLAlchemy
        self.database_url = (
            f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
            f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"
        )
        
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
        """
        get_session Récupère une session de base de données
        :return: Session de base de données
        """
        return self.Session()

    def close_session(self, session):
        """
        close_session Ferme une session de base de données
        :param session: Session de base de données
        """
        if session:
            session.close()

    def dispose(self):
        """
        dispose Ferme la connexion à la base de données
        """
        self.Session.remove()
        self.engine.dispose()
