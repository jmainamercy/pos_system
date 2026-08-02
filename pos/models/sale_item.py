from sqlalchemy import (Integer, Numeric, Column, ForeignKey)
from sqlalchemy.orm import relationship
from database import Base

class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10,2), nullable=False)
    subtotal = Column(Numeric(10,2), nullable=False)

    sale = relationship("Sale", back_populates="saleitem")
    product = relationship("Product", back_populates="saleitem")
    
    