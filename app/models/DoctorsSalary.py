from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class DoctorsSalary(Base):
    __tablename__ = 'DoctorsSalary'
    doctor_id = Column(Integer, ForeignKey('Doctors.id'), primary_key=True)
    sponsored_merch_sold = Column(Integer)
    hours_worked = Column(Integer)
    category_allowance = Column(Integer)
    bonus = Column(Integer)
    salary_per_hour = Column(' salary_per_hour', Integer)