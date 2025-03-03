from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker    
from dotenv import load_dotenv  # Import the load_dotenv function
import os

load_dotenv()
# Replace these values with your actual PostgreSQL credentials  

pp = os.getenv("DATABASE_URL")
DATABASE_URL = pp 
# Create the database engine  
engine = create_engine(DATABASE_URL)  
  
# Create a session factory  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
  
# Base class for ORM models  
Base = declarative_base()  