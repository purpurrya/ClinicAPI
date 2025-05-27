from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class BenefitedClients(Base):
    __tablename__ = 'BenefitedClients'
    client_id = Column(Integer, ForeignKey('Clients.id'), primary_key=True)
    benefit_id = Column(Integer, ForeignKey('Benefits.id'), primary_key=True)