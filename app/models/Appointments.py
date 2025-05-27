from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Appointments(Base):
    __tablename__ = 'Appointments'
    date = Column(Date, primary_key=True)
    time = Column(Time, primary_key=True)
    client_id = Column(Integer, ForeignKey('Clients.id'), primary_key=True)
    doctor_id = Column(Integer, ForeignKey('Doctors.id'), primary_key=True)
    procedure_id = Column(Integer, ForeignKey('Procedures.id'), primary_key=True)
    comment = Column(Text)