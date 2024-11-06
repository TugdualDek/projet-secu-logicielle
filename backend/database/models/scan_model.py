from sqlalchemy import Column, Integer, String, DateTime, text
from .base import Base

class Scan(Base):
    __tablename__ = 'scans'
    
    id = Column(Integer, primary_key=True)
    target_url = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    completed_at = Column(DateTime, nullable=True)
