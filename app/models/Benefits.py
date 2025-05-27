from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, JSON, Text
from app.database import Base

class Benefits(Base):
    __tablename__ = 'Benefits'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    condition = Column(Text)
    discount = Column(' discount', Integer)