from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Doctors(Base):
    __tablename__ = 'Doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    experience = Column(' experience', Integer)
    категория = Column(String(50))
    специализация = Column(String(100))
    ставка = Column(Integer)