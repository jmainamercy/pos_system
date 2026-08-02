from sqlalchemy import (Integer, DateTime, Numeric, Column, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sale_date = Column(DateTime, default=datetime.now, nullable=False)
    total_amount = Column(Numeric(10,2), nullable=False)
    discount = Column(Numeric(10,2), nullable=False)
    final_amount = Column(Numeric(10,2), nullable=False)

    customer =relationship("Customer", back_populates="sale")
    user = relationship("User", back_populates="sale")
    receipt = relationship("Receipt", back_populates="sale")
    payment = relationship("Payment", back_populates="sale")
    saleitem = relationship("SaleItem", back_populates="sale")