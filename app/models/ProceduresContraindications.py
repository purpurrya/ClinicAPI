from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class ProceduresContraindications(Base):
    __tablename__ = 'ProceduresContraindications'
    procedure_id = Column(Integer, ForeignKey('Procedures.id'), primary_key=True)
    contraindication_code = Column(String(10), ForeignKey('Contraindications.code'), primary_key=True)