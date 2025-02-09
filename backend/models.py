# models.py

from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, func  

class User(Base):  
    __tablename__ = "user"  
    user_id = Column(Integer, primary_key=True, index=True)  
    username = Column(String, unique=True, nullable=True, index=True)  # Optional for Google Sign-In users  
    email = Column(String, unique=True, nullable=False, index=True)  
    password = Column(String, nullable=True)  # Optional for Google Sign-In users  
    google_id = Column(String, unique=True, nullable=True)  # New column for Google ID  
    full_name = Column(String, nullable=True)  
    address = Column(String, nullable=True)  
    phone = Column(String, nullable=True)  
    created_at = Column(DateTime, server_default=func.now())  
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  