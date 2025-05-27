from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class ProceduresAnalysis(Base):
    __tablename__ = 'ProceduresAnalysis'
    procedure_id = Column(Integer, ForeignKey('Procedures.id'), primary_key=True)
    analysis_id = Column(Integer, ForeignKey('Analysis.id'), primary_key=True)