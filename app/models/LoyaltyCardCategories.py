from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class LoyaltyCardCategories(Base):
    __tablename__ = 'LoyaltyCardCategories'
    id = Column(Integer, primary_key=True)
    category = Column(Integer, nullable=False)
    condition = Column(Text)
    discount = Column(Integer)