from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
from .base import Base

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id', ondelete='CASCADE'))
    vulnerability_type = Column(String(100))
    severity = Column(String(50))
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
