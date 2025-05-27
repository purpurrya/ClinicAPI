from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Supplies(Base):
    __tablename__ = 'Supplies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    amount = Column(Integer)
    last_delivery_date = Column(Date)
    purchase_price = Column(' purchase_price', Integer)
    supplier_id = Column(Integer, ForeignKey('Suppliers.id'))