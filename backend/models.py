# models.py

from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "user"  # Table name in your database

    # Primary Key: auto-incremented user_id
    user_id = Column(Integer, primary_key=True, index=True)
    
    # User information columns
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # Timestamps: using SQLAlchemy's server default functions
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
