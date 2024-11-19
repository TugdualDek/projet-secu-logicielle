from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text, Text
from sqlalchemy.orm import relationship
from backend.database.models.base import Base

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id', ondelete='CASCADE'))
    vulnerability_type = Column(String(250))
    vulnerability_name = Column(String(250))
    additional_info = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)

    #create a relationship between report and scan
    scan = relationship('Scan', back_populates='reports')

    # Méthode pour convertir l'objet en dictionnaire
    def to_dict(self):
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'vulnerability_type': self.vulnerability_type,
            'vulnerability_name': self.vulnerability_name,
            'description': self.description,
            'created_at': self.created_at
        }