from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class ClientsContraindications(Base):
    __tablename__ = 'ClientsContraindications'
    client_id = Column(Integer, ForeignKey('Clients.id'), primary_key=True)
    contraindication_code = Column(String(10), ForeignKey('Contraindications.code'), primary_key=True)
