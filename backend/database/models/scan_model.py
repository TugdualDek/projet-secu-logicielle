import json
from sqlalchemy import Column, Integer, String, DateTime, text, Text, Enum
from backend.database.models.base import Base
from sqlalchemy.orm import relationship

class Scan(Base):
    __tablename__ = 'scans'
    
    id = Column(Integer, primary_key=True)
    target_url = Column(String(255), nullable=False)
    status = Column(Enum('pending', 'completed', 'in_progress', 'failed', name='scan_status'), default='pending')
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    #create a relationship between scan and report
    reports = relationship('Report', back_populates='scan', cascade='all, delete-orphan')

    # Méthode pour convertir l'objet en dictionnaire
    def to_dict(self):
        return {
            'id': self.id,
            'target': self.target_url,
            'status': self.status,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }