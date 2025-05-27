from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Wards(Base):
    __tablename__ = 'Wards'
    id = Column(Integer, primary_key=True)
    category = Column(String(50))
    price_per_day = Column(Integer)
    occupancy = Column(Boolean)