from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Hospital(Base):
    __tablename__ = 'Hospital'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('Clients.id'))
    receipt_date = Column(Date)
    discharge_date = Column(Date)
    ward_id = Column(Integer, ForeignKey('Wards.id'))
    service_id = Column(Integer, ForeignKey('HospitalServices.id'))
    payment_sum = Column(Integer)