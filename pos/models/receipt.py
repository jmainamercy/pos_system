from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(
        Integer, primary_key=True, nullable=False, index=True, autoincrement=True
    )
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    receipt_number = Column(String, nullable=False)
    issued_at = Column(DateTime, nullable=False, default=datetime.now)

    sale = relationship("Sale", back_populates="receipt")
