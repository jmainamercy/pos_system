from sqlalchemy import (Integer, String, Column)
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    loyalty_points = Column(Integer, nullable=False, default=0)

    sale = relationship("Sale", back_populates="customer")
    

