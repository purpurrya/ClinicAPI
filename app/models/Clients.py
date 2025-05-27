from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Clients(Base):
    __tablename__ = 'Clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(11))
    email = Column(String(100))
    date_of_birth = Column(Date)
    loyalty_card_category = Column(Integer, ForeignKey('LoyaltyCardCategories.id'))