

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils import auth_utils, create_access_token, verify_token  # Fixed import
from schemas import UserCreate, Token
from datetime import timedelta
import os

from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from utils import auth_utils, create_access_token
from sqlalchemy.orm import sessionmaker
from database import engine


app = FastAPI()

# Dependency injection for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return access token"""
    hashed_password = auth_utils.hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        address=user.address,
        phone=user.phone
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def login(email: str, password: str, db: Session = Depends(SessionLocal)):
    """Authenticate user and return JWT token"""
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not auth_utils.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected-route")
async def protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(SessionLocal)):
    """A route protected by JWT authentication"""
    user_email = verify_token(token)

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Access granted", "user": user}


### Google OAuth2 Sign-in ###
@app.get("/google-auth-url")
async def google_auth_url():
    """Return Google OAuth authorization URL"""
    return {"auth_url": auth_utils.get_google_auth_url()}

@app.post("/google-login", response_model=Token)
async def google_login(google_token: str):
    """Verify Google token and return JWT token"""
    user_info = auth_utils.verify_google_token(google_token)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
    # Generate JWT token for authenticated user
    access_token = create_access_token(data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=30))
    
    return {"access_token": access_token, "token_type": "bearer", "user_info": user_info}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)



# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from utils import auth_utils, create_access_token, verify_token, oauth2_scheme  # Ensure correct imports
# from schemas import UserCreate, Token
# from datetime import timedelta
# import os

# app = FastAPI()

# # Dependency injection for authentication
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


# @app.post("/register", response_model=Token)
# async def register(user: UserCreate):
#     """Register a new user and return access token"""
#     hashed_password = auth_utils.hash_password(user.password)
    
#     # Here you would store user data in a database (mocked for now)
#     user_data = {
#         "username": user.username,
#         "email": user.email,
#         "password": hashed_password,  # Store hashed password
#         "full_name": user.full_name,
#         "address": user.address,
#         "phone": user.phone
#     }

#     # Generate access token
#     access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/login", response_model=Token)
# async def login(email: str, password: str):
#     """Authenticate user and return JWT token"""
    
#     # Normally, you'd fetch the user from the database
#     # For now, we assume the user exists and use a mock password hash
#     stored_hashed_password = auth_utils.hash_password("mockpassword")  

#     if not auth_utils.verify_password(password, stored_hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     # Create JWT token
#     access_token = create_access_token(data={"sub": email}, expires_delta=timedelta(minutes=30))
    
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/protected-route")
# async def protected_route(token: str = Depends(oauth2_scheme)):
#     """A route protected by JWT authentication"""
#     user_email = verify_token(token)  # Decode the token
#     return {"message": "Access granted", "user_email": user_email}


# ### Google OAuth2 Sign-in ###
# @app.get("/google-auth-url")
# async def google_auth_url():
#     """Return Google OAuth authorization URL"""
#     return {"auth_url": auth_utils.get_google_auth_url()}

# @app.post("/google-login", response_model=Token)
# async def google_login(google_token: str):
#     """Verify Google token and return JWT token"""
#     user_info = auth_utils.verify_google_token(google_token)
    
#     if not user_info:
#         raise HTTPException(status_code=401, detail="Invalid Google token")
    
#     # Generate JWT token for authenticated user
#     access_token = create_access_token(data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=30))
    
#     return {"access_token": access_token, "token_type": "bearer", "user_info": user_info}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)



















# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.responses import RedirectResponse
# from sqlalchemy.orm import Session
# from database import SessionLocal
# import models
# import schemas
# from utils import auth_utils , create_access_token, verify_token, oauth2_scheme # Corrected import

# from fastapi.security import OAuth2PasswordRequestForm

# from datetime import timedelta

# from utils import auth_utils, oauth2_scheme  # Remove create_access_token, verify_token





# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# class AuthService:

#     def __init__(self, db: Session):
#         self.db = db
        
#     def authenticate_user(self, email: str, password: str):
#         user = self.db.query(models.User).filter(models.User.email == email).first()
#         if not user or not auth_utils.verify_password(password, user.password):
#             return None
#         return user



#     def google_sign_in(self, code: str):
#         user_info = auth_utils.get_user_info(code)  # Corrected method call
#         if not user_info:
#             raise HTTPException(status_code=400, detail="Invalid Google authentication")

#         email = user_info.get("email")
#         google_id = user_info.get("id")  # Google returns "id" instead of "google_id"
#         full_name = user_info.get("name")

#         db_user = self.db.query(models.User).filter(models.User.email == email).first()
#         if db_user:
#             if not db_user.google_id:
#                 db_user.google_id = google_id
#                 self.db.commit()
#                 self.db.refresh(db_user)
#             return db_user

#         new_user = models.User(
#             google_id=google_id,
#             email=email,
#             full_name=full_name,
#             username=None,
#             password=None,
#         )
#         self.db.add(new_user)
#         self.db.commit()
#         self.db.refresh(new_user)
#         return new_user

#     def register_user(self, user: schemas.UserCreate):
#         existing_user = self.db.query(models.User).filter(
#             (models.User.email == user.email) | (models.User.username == user.username)
#         ).first()
#         if existing_user:
#             raise HTTPException(
#                 status_code=400, detail="A user with this email or username already exists"
#             )

#         hashed_password = auth_utils.hash_password(user.password)  # Corrected call
#         new_user = models.User(
#             username=user.username,
#             email=user.email,
#             password=hashed_password,
#             full_name=user.full_name,
#             address=user.address,
#             phone=user.phone,
#             role="customer"
#         )
#         self.db.add(new_user)
#         self.db.commit()
#         self.db.refresh(new_user)
#         return new_user
    
    
    
    
    
    

# @app.post("/login", response_model=schemas.Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     auth_service = AuthService(db)
#     user = auth_service.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/auth/callback")
# def google_auth_callback(code: str, db: Session = Depends(get_db)):
#     user = AuthService(db).google_sign_in(code)
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/register", response_model=schemas.UserOut)
# def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return AuthService(db).register_user(user)

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     email = verify_token(token)
#     user = db.query(models.User).filter(models.User.email == email).first()
#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user

# @app.post("/create-brand", response_model=schemas.BrandOut)
# def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     new_brand = models.Brand(**brand.dict())
#     db.add(new_brand)
#     db.commit()
#     db.refresh(new_brand)
#     return new_brand

# @app.post("/post-product", response_model=schemas.ProductOut)
# def post_product(product: schemas.ProductCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     brand = db.query(models.Brand).filter(models.Brand.brand_id == product.brand_id).first()
#     if not brand:
#         raise HTTPException(status_code=400, detail="Brand ID does not exist")
#     new_product = models.Product(**product.dict())
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product
    
    
    
    
    


# @app.get("/login/google")
# def login_google():
#     return RedirectResponse(auth_utils.get_google_auth_url())  # Corrected method call

# @app.get("/auth/callback")
# def google_auth_callback(code: str, db: Session = Depends(get_db)):
#     return AuthService(db).google_sign_in(code)

# @app.post("/register", response_model=schemas.UserOut)
# def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return AuthService(db).register_user(user)

# @app.post("/create-brand", response_model=schemas.BrandOut)
# def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.user_id == brand.user_id).first()
#     if not user:
#         raise HTTPException(status_code=400, detail="User ID does not exist")
#     new_brand = models.Brand(**brand.dict())
#     db.add(new_brand)
#     db.commit()
#     db.refresh(new_brand)
#     return new_brand

# @app.post("/post-product", response_model=schemas.ProductOut)
# def post_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
#     brand = db.query(models.Brand).filter(models.Brand.brand_id == product.brand_id).first()
#     if not brand:
#         raise HTTPException(status_code=400, detail="Brand ID does not exist")
#     new_product = models.Product(**product.dict())
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product
