from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
from backend.database.models.base import Base

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id', ondelete='CASCADE'))
    vulnerability_type = Column(String(250))
    vulnerability_name = Column(String(250))
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
