from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    barcode = Column(String,unique=True, nullable=False)
    name = Column(String, nullable=False)
    price =  Column(Numeric(10,2), nullable=False)
    cost_price = Column(Numeric(10,2), nullable= False)
    stock_qty = Column(Integer, nullable=False)

    category = relationship("Category", back_populates="product")
    supplier = relationship("Supplier", back_populates="product")
    saleitem = relationship("SaleItem", back_populates="product")
    