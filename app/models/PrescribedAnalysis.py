from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class PrescribedAnalysis(Base):
    __tablename__ = 'PrescribedAnalysis'
    client_id = Column(Integer, ForeignKey('Clients.id'), primary_key=True)
    analysis_id = Column(Integer, ForeignKey('Analysis.id'), primary_key=True)
    results = Column(JSON)