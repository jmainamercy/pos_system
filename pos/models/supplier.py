from sqlalchemy import (Integer, String, Text, Column)
from sqlalchemy.orm import relationship
from database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, nullable=False, index=True,autoincrement=True)
    company_name = Column(String(50), nullable=False)
    contact_name = Column(String(150), nullable=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=True)

    product = relationship("Product", back_populates="supplier")

