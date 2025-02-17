


from fastapi import FastAPI, Depends, HTTPException,Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from schemas import UserCreate, Token
from utils import auth_utils, create_access_token, verify_token
from datetime import timedelta
import os
import dotenv
from pydantic import BaseModel
import uvicorn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from utils import verify_token


dotenv.load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
if not GOOGLE_CLIENT_ID:
    raise ValueError("GOOGLE_CLIENT_ID is not set in environment variables.")


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    email: str
    password: str


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
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not auth_utils.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected-route")
def protected_route(token_data: dict = Depends(verify_token)):
    return {"message": "Welcome to the protected route!", "user": token_data}



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
    
    access_token = create_access_token(data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer", "user_info": user_info}

@app.get("/test-headers")
async def test_headers(authorization: str = Header(None)):
    return {"Authorization Header": authorization}





def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Retrieve the currently authenticated user from JWT token."""
    user_email = verify_token(token)
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user

@router.post("/create-brand", response_model=schemas.BrandOut)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """
    Allows a logged-in user to create a brand.
    - The user must be authenticated.
    - The user ID is fetched from the JWT token and assigned to the brand.
    """

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")

    new_brand = models.Brand(
        user_id=user.user_id,
        brand_name=brand.brand_name,
        brand_description=brand.brand_description,
        logo=brand.logo
    )

    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand

@router.post("/post-product", response_model=schemas.ProductOut)
def post_product(product: schemas.ProductCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """
    Allows a user to post a product under a brand.
    - The user must be logged in.
    - The brand must exist.
    - The brand must belong to the authenticated user.
    """

   
    brand = db.query(models.Brand).filter(models.Brand.brand_id == product.brand_id).first()
    
    if not brand:
        raise HTTPException(status_code=400, detail="Brand does not exist.")

    
    if brand.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to add products to this brand.")

    new_product = models.Product(
        brand_id=product.brand_id,
        product_name=product.product_name,
        product_pic=product.product_pic,
        product_video=product.product_video,
        category=product.category,
        description=product.description,
        order_size=product.order_size,
        order_quantity=product.order_quantity,
        quantity_unit=product.quantity_unit,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)



