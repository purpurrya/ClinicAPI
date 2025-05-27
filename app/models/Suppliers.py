from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Suppliers(Base):
    __tablename__ = 'Suppliers'
    id = Column(Integer, primary_key=True)
    company = Column(String(255), nullable=False)
    city = Column(String(100))
    type_of_supply = Column(String(100))
    email = Column(Text)