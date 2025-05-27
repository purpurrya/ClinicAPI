from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Sponsors(Base):
    __tablename__ = 'Sponsors'
    id = Column(Integer, primary_key=True)
    company = Column(String(255), nullable=False)
    products = Column(String(100))
    sales_percentage = Column(Integer)
    last_delivery_date = Column(Date)
    sold = Column(Integer)
    email = Column(Text)