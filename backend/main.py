


from fastapi import FastAPI, Depends, HTTPException,Header, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from schemas import UserCreate, Token, LoginRequest, UserUpdate, OrderOut, OrderCreate
from utils import auth_utils, create_access_token, verify_token, create_email_verification_token, send_verification_email
from datetime import timedelta
import os
import dotenv
from pydantic import BaseModel
import uvicorn
from typing import Annotated, List
from models import Order, OrderItem, Bill  

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from utils import verify_token

from fastapi import Depends, FastAPI, HTTPException, status
import jwt


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import JSONResponse

from typing import Annotated


dotenv.load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
if not GOOGLE_CLIENT_ID:
    raise ValueError("GOOGLE_CLIENT_ID is not set in environment variables.")

router = APIRouter()  

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





def authenticate_user(db: Session, username: str, password: str):  
    """  
    Authenticate the user by username and password.  
    Returns the user object if authentication is successful, otherwise returns False.  
    """  
    # Query the database for the user by username  
    user = db.query(User).filter(User.username == username).first()  
    
    print(user)
    if not user:  
        return False  # User does not exist  
    # Verify the password  
    if not auth_utils.verify_password(password, user.password):  
        return False  # Password is incorrect  
    return user  # User is authenticated  


@app.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and send a verification email"""

    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists.")

    hashed_password = auth_utils.hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        address=user.address,
        phone=user.phone,
        is_verified=False  
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # ✅ Generate verification token
    token = create_email_verification_token(user.email)

    # ✅ Send verification email
    await send_verification_email(user.email, token)

    return JSONResponse(status_code=200, content={"message": "Verification email sent. Please check your inbox."})



@app.post("/login", response_model=Token)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not auth_utils.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}





@app.post("/protected-route")  
def protected_route(token: str = Depends(oauth2_scheme), token_data: dict = Depends(verify_token)):  
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











# Authenticate user from DB
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not auth_utils.verify_password(password, user.password):
        return False
    return user



# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# View Profile
@app.get("/profile")
def get_profile(user: User = Depends(get_current_user)):
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "phone": user.phone,
    }

# Update Profile
@app.put("/update-profile")
def update_profile(user_update: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.full_name:
        db_user.full_name = user_update.full_name
    if user_update.address:
        db_user.address = user_update.address
    if user_update.phone:
        db_user.phone = user_update.phone

    db.commit()
    db.refresh(db_user)
    return {"message": "Profile updated successfully"}



# Create Brand (protected route)
@app.post("/create-brand", response_model=schemas.BrandOut)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    
    
    existing_brand = db.query(models.Brand).filter(models.Brand.user_id == User.user_id).first()
    #print(existing_brand.brand_name)
    
    if existing_brand:
        raise HTTPException(status_code=400, detail="You can create only one brand.")


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


@app.get("/brands/me", response_model=schemas.BrandOut)
def get_my_brand(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    brand = db.query(models.Brand).filter(models.Brand.user_id == current_user.user_id).first()
    
    if not brand:
        raise HTTPException(status_code=404, detail="You have not created a brand")
    
    return brand





@app.put("/brands/{brand_id}", response_model=schemas.BrandOut)
def update_brand(brand_id: int, brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    db_brand = db.query(models.Brand).filter(models.Brand.brand_id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    db_brand.brand_name = brand.brand_name
    db_brand.brand_description = brand.brand_description
    db_brand.logo = brand.logo

    db.commit()
    db.refresh(db_brand)
    return db_brand




# Post Product (protected route)
@app.post("/post-product", response_model=schemas.ProductCreate)
def post_product(product: schemas.ProductCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user), current_user: models.User = Depends(get_current_user)):
    
    brand = db.query(models.Brand).filter(models.Brand.user_id == current_user.user_id).first()
    print(brand.brand_id)
     
    if not brand:
        raise HTTPException(status_code=400, detail="Brand does not exist.")
    if brand.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to add products to this brand.")

    new_product = models.Product(
        brand_id=brand.brand_id,

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



@app.put("/update-product/{product_id}", response_model=schemas.ProductCreate)
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    
    # Update product fields
    product.product_name = updated_product.product_name
    product.product_pic = updated_product.product_pic
    product.product_video = updated_product.product_video
    product.category = updated_product.category
    product.description = updated_product.description
    product.order_size = updated_product.order_size
    product.order_quantity = updated_product.order_quantity
    product.quantity_unit = updated_product.quantity_unit
    product.price = updated_product.price

    db.commit()
    db.refresh(product)
    return product



@app.get("/get-product/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return product



@app.get("/get-all-products", response_model=List[schemas.ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

  
@app.post("/orders", response_model=OrderOut)  
def create_order(order: OrderCreate, db: Session = Depends(get_db)):  
    """Create a new order"""  
    db_order = Order(user_id=order.user_id, status=order.status)  
    db.add(db_order)  
    db.commit()  
    db.refresh(db_order)  
  
    # Add order items  
    for item in order.order_items:  
        db_order_item = OrderItem(  
            order_id=db_order.order_id,  
            product_id=item.product_id,  
            size=item.size,  
            quantity=item.quantity  
        )  
        db.add(db_order_item)  
  
    # Add bill  
    db_bill = Bill(  
        order_id=db_order.order_id,  
        amount=order.bill.amount,  
        method=order.bill.method,  
        trx_id=order.bill.trx_id,  
        status=order.bill.status  
    )  
    db.add(db_bill)  
  
    db.commit()  
    db.refresh(db_order)  
    return db_order  



  
@app.get("/orders/{user_id}", response_model=List[OrderOut])  
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):  
    """Retrieve all orders for a specific user"""  
    orders = db.query(Order).filter(Order.user_id == user_id).all()  
    if not orders:  
        raise HTTPException(status_code=404, detail="No orders found for this user")  
    return orders  
  
@app.get("/order/{order_id}", response_model=OrderOut)  
def get_order(order_id: int, db: Session = Depends(get_db)):  
    """Retrieve a specific order by order_id"""  
    order = db.query(Order).filter(Order.order_id == order_id).first()  
    if not order:  
        raise HTTPException(status_code=404, detail="Order not found")  
    return order  
  
# --- Utility Functions ---  
  
# Include token creation and verification functions here  
# Example: `create_access_token`, `verify_token`  




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)








