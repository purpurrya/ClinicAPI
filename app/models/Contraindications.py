from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Contraindications(Base):
    __tablename__ = 'Contraindications'
    code = Column(String(10), primary_key=True)
    name = Column(String(255), nullable=False)