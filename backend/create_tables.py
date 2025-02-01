# create_tables.py

from database import engine, Base
import models # This will register the User model with Base

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
