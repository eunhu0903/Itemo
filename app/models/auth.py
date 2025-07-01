from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    oauth_id = Column(Integer, unique=True, index=True, nullable=False)
    oauth_provider = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    username = Column(String(20), nullable=True)
    profile_image = Column(String(255), nullable=True)
    google_profile_image = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    shipping_addresses = relationship("ShippingAddress", back_populates="user")
