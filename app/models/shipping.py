from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class ShippingAddress(Base):
    __tablename__ = "shipping_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(255), nullable=True)
    detail_address = Column(String(255), nullable=False)
    postal_code = Column(String(20), nullable=False)
    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="shipping_addresses")
