from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Staff(Base):
    __tablename__ = 'Staff'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    experience = Column(Integer)
    post = Column(String(100))
    bid = Column(Integer)
    salary_per_hour = Column(Integer)
    hours_worked = Column(Integer)
    additional_payment = Column(Integer)