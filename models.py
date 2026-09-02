from sqlalchemy import Column, Integer, String, Text
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # approved, pending, rejected
    image_url = Column(String(500), nullable=True)