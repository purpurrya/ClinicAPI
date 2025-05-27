from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Payments(Base):
    __tablename__ = 'Payments'
    id = Column(Integer, primary_key=True)
    date_of_payment = Column(Date)
    client_id = Column(Integer, ForeignKey('Clients.id'))
    procedure_id = Column(Integer, ForeignKey('Procedures.id'))
    sum = Column(Integer)
    payment_method = Column(String(50))
    status = Column(Boolean)