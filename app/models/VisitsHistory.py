from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class VisitsHistory(Base):
    __tablename__ = 'VisitsHistory'
    client_id = Column(Integer, ForeignKey('Clients.id'), primary_key=True)
    doctor_id = Column(Integer, ForeignKey('Doctors.id'), primary_key=True)
    procedure_id = Column(Integer, ForeignKey('Procedures.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    time = Column(Time, primary_key=True)
    price = Column(Integer)
    doctors_report = Column(Text)