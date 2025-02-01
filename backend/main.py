# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas
from passlib.context import CryptContext

# Create the database tables (if they don't already exist)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET endpoint to retrieve all users (optional)
@app.get("/users", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# POST endpoint to create a new user
@app.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if a user with the same username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password before saving it
    hashed_password = get_password_hash(user.password)
    
    # Create a new User instance
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        address=user.address,
        phone=user.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
