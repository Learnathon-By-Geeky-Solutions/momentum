


from fastapi import FastAPI, Depends, HTTPException,Header, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from schemas import UserCreate, Token, LoginRequest, UserUpdate, OrderOut, OrderCreate, PayBillRequest, ForgotPasswordRequest, ResetPasswordRequest
from utils import auth_utils, create_access_token, verify_token, create_email_verification_token, send_verification_email, verify_reset_token, create_reset_token, send_reset_email
from datetime import timedelta
import os
import dotenv
from pydantic import BaseModel
import uvicorn
from typing import Annotated, List, Optional
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
from decimal import Decimal


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

from fastapi import BackgroundTasks

@app.post("/forgot-password")
def forgot_password(request_data: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request_data.email).first()
    
    # For security, return the same message even if the user is not found.
    if not user:
        return {"message": "If the email exists, a password reset link has been sent."}
    
    reset_token = create_reset_token(user.email)
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
    
    # Use background tasks to send the email asynchronously
    background_tasks.add_task(send_reset_email, user.email, reset_link)
    
    return {"message": "If the email exists, a password reset link has been sent."}

    

@app.post("/reset-password")
def reset_password(request_data: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = verify_reset_token(request_data.token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Hash the new password and update
    hashed_password = auth_utils.hash_password(request_data.new_password)
    user.password = hashed_password
    db.commit()
    
    return {"message": "Password reset successful. You can now log in with your new password."}



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
    
    
    existing_brand = db.query(models.Brand).filter(models.Brand.user_id == user.user_id).first()

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





@app.put("/updatebrands/me", response_model=schemas.BrandOut)
def update_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    

    db_brand = db.query(models.Brand).filter(models.Brand.user_id == current_user.user_id).first()
    
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


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Retrieve the product by its ID
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Retrieve the brand associated with the product
    brand = db.query(models.Brand).filter(models.Brand.brand_id == product.brand_id).first()
    # Ensure the current user owns this brand
    if not brand or brand.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this product")
    
    # Check for any pending order items for this product.
    # This joins OrderItem and Order, and checks if there is any order with status "Pending"
    pending_order_item = (
        db.query(models.OrderItem)
          .join(models.Order, models.OrderItem.order_id == models.Order.order_id)
          .filter(
              models.OrderItem.product_id == product_id,
              models.Order.status == "Pending"
          )
          .first()
    )
    
    if pending_order_item:
        raise HTTPException(status_code=400, detail="Complete the order before deleting this product.")
    
    # If no pending order is found, delete the product.
    db.delete(product)
    db.commit()
    
    return {"detail": "Product deleted successfully."}









@app.post("/orders", response_model=schemas.OrderOut)
def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new order using the current user's id.
    The order is created based on order items (product id, size, quantity).
    The bill amount is calculated automatically as the sum of (product price * quantity)
    for all order items.
    """
    # Create a new order for the current user
    db_order = models.Order(
        user_id=current_user.user_id,
        status="Pending"  # Set initial status as "Pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    total_amount = 0

    # Process each order item
    for item in order.order_items:
        # Retrieve product information to calculate the cost
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        
        # (Optional) Check if there's enough stock
        if product.order_quantity is not None and item.quantity > product.order_quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.product_name}")
        
        # Calculate cost for this item (assuming product.price is of type DECIMAL/float)
        item_cost = float(product.price) * item.quantity
        total_amount += item_cost

        # Create a new order item record
        db_order_item = models.OrderItem(
            order_id=db_order.order_id,
            product_id=item.product_id,
            size=item.size,
            quantity=item.quantity
        )
        db.add(db_order_item)
        
    total_amount = Decimal(total_amount)
    # Create the Bill record with the calculated total amount
    db_bill = models.Bill(
        order_id=db_order.order_id,
        amount=total_amount,
        method="Pending",  # you may update this later (e.g., "Cash on Delivery", "Credit Card")
        trx_id="1234",
        status="Pending"
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_order)
    return db_order




@app.get("/orders/me")
def get_my_orders(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    
    # For constructing the links we use a base URL.
    # In a real app, you might use request.url_for or an environment variable.
    base_url = "http://127.0.0.1:8000"

    
    orders_with_links = []
    for order in orders:
        order_data = {
            "order_id": order.order_id,
            "user_id": order.user_id,
            "status": order.status,
            # Link to view full order details (e.g., order summary, bill, etc.)
            "order_details_url": f"{base_url}/order/{order.order_id}",
            # Link to view product details for items in this order
            "product_details_url": f"{base_url}/order/{order.order_id}/products"
        }
        orders_with_links.append(order_data)
        print(order_data)
    
    return orders_with_links



@app.get("/order/{order_id}/bill", response_model=schemas.BillOut)
def get_bill_for_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Retrieve the bill information for a given order.
    Ensures the order belongs to the current user.
    """
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to view this order's bill")

    bill = db.query(models.Bill).filter(models.Bill.order_id == order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")
    return bill

  
  
@app.get("/order/{order_id}/details", response_model=schemas.OrderDetailOut)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get the order ensuring it belongs to the current user
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id,
        models.Order.user_id == current_user.user_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Get the bill for this order
    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()

    # Retrieve order items with product and brand details.
    # We join OrderItem with Product and then join Product with Brand.
    order_items_query = db.query(
        models.OrderItem,
        models.Product,
        models.Brand
    ).join(
        models.Product, models.OrderItem.product_id == models.Product.product_id
    ).join(
        models.Brand, models.Product.brand_id == models.Brand.brand_id
    ).filter(
        models.OrderItem.order_id == order.order_id
    ).all()

    order_items = []
    for order_item, product, brand in order_items_query:
        item_data = {
            "product_id": product.product_id,
            "brand_id": brand.brand_id,
            "product_name": product.product_name,
            "brand_name": brand.brand_name,
            "order_size": order_item.size,  # assuming OrderItem has a column 'size'
            "order_quantity": order_item.quantity
        }
        order_items.append(item_data)

    # Construct the output data
    result = {
        "order_id": order.order_id,
        "status": order.status,
        "created_at": order.created_at,
        "bill_amount": bill.amount if bill else None,
        "order_items": order_items
    }
    return result




@app.get("/orders/me/details", response_model=List[schemas.OrderDetailOut])
def get_all_order_details(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all orders for the current user, including:
    - Order id, status, created_at, bill amount
    - A list of order items with product and brand details
    """
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    
    orders_details = []
    for order in orders:
        # Retrieve the bill for this order
        bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
        #print(bill)
        # Retrieve order items along with product and brand details
        order_items_query = db.query(
            models.OrderItem,
            models.Product,
            models.Brand
        ).join(
            models.Product, models.OrderItem.product_id == models.Product.product_id
        ).join(
            models.Brand, models.Product.brand_id == models.Brand.brand_id
        ).filter(
            models.OrderItem.order_id == order.order_id
        ).all()
        
        

        order_items = []
        for order_item, product, brand in order_items_query:
            item_data = {
                "product_id": product.product_id,
                "brand_id": brand.brand_id,
                "product_name": product.product_name,
                "brand_name": brand.brand_name,
                "order_size": order_item.size,  # Adjust if your column name is different
                "order_quantity": order_item.quantity
            }
            order_items.append(item_data)

        order_data = {
            "order_id": order.order_id,
            "status": order.status,
            "bill_status": bill.status if bill else None,
            "created_at": order.created_at,
            "bill_amount": bill.amount if bill else None,
            "order_items": order_items
        }
        orders_details.append(order_data)
    
    return orders_details


@app.delete("/order/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Retrieve the order ensuring it belongs to the current user
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id,
        models.Order.user_id == current_user.user_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Retrieve the associated bill for this order
    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")
    
    # Check if the bill's status is still "Pending" (case-insensitive)
    if bill.status.lower() != "pending":
        raise HTTPException(
            status_code=400,
            detail="Cannot delete order: bill is already confirmed or processed."
        )
    
    # Delete the order (if cascading is set up, related order items and bill might be deleted automatically)
    db.delete(order)
    db.commit()
    
    return {"detail": "Order deleted successfully."}






@app.post("/paybill")
def pay_bill(
    paybill_data: schemas.PayBillRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Confirm payment for an order:
      - Update the bill with the given method and trx_id, and mark its status as confirmed.
      - Decrease the stock (order_quantity) of each product based on the quantities in the order items.
    """
    # 1. Retrieve the order ensuring it belongs to the current user.
    order = db.query(models.Order).filter(
        models.Order.order_id == paybill_data.order_id,
        models.Order.user_id == current_user.user_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # 2. Retrieve the corresponding bill
    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")
    
    # 3. Update bill details: set the method, trx_id, and update status to "Confirmed"
    bill.method = paybill_data.method
    bill.trx_id = paybill_data.trx_id
    bill.status = "Confirmed"  # or "True" if you prefer, but using a descriptive status is better
    db.add(bill)
    db.commit()
    
    # 4. For each order item, decrease the product's available stock.
    order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.order_id).all()
    for item in order_items:
        # Retrieve the product corresponding to the order item
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if product and product.order_quantity is not None:
            # Decrease the product stock by the ordered quantity
            new_stock = product.order_quantity - item.quantity
            # Ensure stock doesn't go negative
            product.order_quantity = new_stock if new_stock >= 0 else 0
            db.add(product)
    
    db.commit()
    
    return {"message": "Bill confirmed and product stocks updated successfully."}

  



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)








