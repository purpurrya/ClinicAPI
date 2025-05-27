from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class ProceduresSupplies(Base):
    __tablename__ = 'ProceduresSupplies'
    procedure_id = Column(Integer, ForeignKey('Procedures.id'), primary_key=True)
    supply_id = Column(Integer, ForeignKey('Supplies.id'), primary_key=True)