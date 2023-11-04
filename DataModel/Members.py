from sqlalchemy import Column, Integer, String, Float, Date
from DataModel.BaseDM import BaseDM
class Members(BaseDM):
    __tablename__ = 'Members'
    Name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    due_amount = Column(Float)
