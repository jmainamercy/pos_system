from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
    )

    product = relationship("Product", back_populates="category")
