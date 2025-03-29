<<<<<<< HEAD


from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Annotated
from decimal import Decimal
import schemas as schemas
import models as models
from models import Order, OrderItem, Product, User, Brand
from database import get_db, SessionLocal
from utils import get_current_user  



=======
<<<<<<< HEAD


from fastapi import FastAPI, Depends, HTTPException, APIRouter
=======
from fastapi import FastAPI, Depends, HTTPException
>>>>>>> 54066bc9f1766879eb45177911b2216d15f00273
from sqlalchemy.orm import Session
from typing import List, Annotated
from decimal import Decimal
<<<<<<< HEAD
import schemas as schemas
import models as models
from models import Order, OrderItem, Product, User, Brand
from schemas import UserCreate, Token, LoginRequest, UserUpdate, OrderOut, OrderCreate, PayBillRequest, ForgotPasswordRequest, ResetPasswordRequest
from models import Product, Order, User, OrderItem, Bill
from database import get_db
from utils import get_current_user  # Adjust path based on your project structure
from database import SessionLocal



=======
from fastapi import APIRouter
>>>>>>> 54066bc9f1766879eb45177911b2216d15f00273

from user_management import schemas, models
from user_management.database import get_db
from user_management.utils import get_current_user
from user_management.models import Order, Product
from user_management.database import SessionLocal
>>>>>>> backend


router = APIRouter()


<<<<<<< HEAD

@router.post("/orders", response_model=schemas.OrderOut)
async def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
=======
<<<<<<< HEAD

=======
>>>>>>> 54066bc9f1766879eb45177911b2216d15f00273
@router.post("/orders", response_model=schemas.OrderOut)
async def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
>>>>>>> backend
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
<<<<<<< HEAD
        status="Pending"  # Set initial status as "Pending"
=======
        status="Pending",  # Set initial status as "Pending"
>>>>>>> backend
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
<<<<<<< HEAD
    
=======

>>>>>>> backend
    total_amount = 0

    # Process each order item
    for item in order.order_items:
        # Retrieve product information to calculate the cost
<<<<<<< HEAD
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        
        # (Optional) Check if there's enough stock
        if product.order_quantity is not None and item.quantity > product.order_quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.product_name}")
        
=======
        product = (
            db.query(models.Product)
            .filter(models.Product.product_id == item.product_id)
            .first()
        )
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product with id {item.product_id} not found"
            )

        # (Optional) Check if there's enough stock
        if (
            product.order_quantity is not None
            and item.quantity > product.order_quantity
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.product_name}",
            )

>>>>>>> backend
        # Calculate cost for this item (assuming product.price is of type DECIMAL/float)
        item_cost = float(product.price) * item.quantity
        total_amount += item_cost

        # Create a new order item record
        db_order_item = models.OrderItem(
            order_id=db_order.order_id,
            product_id=item.product_id,
            size=item.size,
<<<<<<< HEAD
            quantity=item.quantity
        )
        db.add(db_order_item)
        
=======
            quantity=item.quantity,
        )
        db.add(db_order_item)

>>>>>>> backend
    total_amount = Decimal(total_amount)
    # Create the Bill record with the calculated total amount
    db_bill = models.Bill(
        order_id=db_order.order_id,
        amount=total_amount,
        method="Pending",  # you may update this later (e.g., "Cash on Delivery", "Credit Card")
        trx_id="1234",
<<<<<<< HEAD
        status="Pending"
=======
        status="Pending",
>>>>>>> backend
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_order)
    return db_order


<<<<<<< HEAD




=======
>>>>>>> backend
def place_order(user_id, product_id, size, quantity=1):
    """
    Places an order for a product.
    """
    session = SessionLocal()
    try:
        # Fetch product details
<<<<<<< HEAD
        product = session.query(Product).filter(
            Product.product_id == product_id,
            Product.order_size == size  # Ensure correct size is ordered
        ).first()
=======
        product = (
            session.query(Product)
            .filter(
                Product.product_id == product_id,
                Product.order_size == size,  # Ensure correct size is ordered
            )
            .first()
        )
>>>>>>> backend

        if not product:
            return "Product not found or size unavailable."

        # Check stock availability
        if product.order_quantity < quantity:
            return f"Sorry, only {product.order_quantity} items left in stock."

        # Create a new order
        new_order = Order(
            user_id=user_id,
            product_id=product_id,
            size=size,
            quantity=quantity,
<<<<<<< HEAD
            total_price=product.price * quantity
=======
            total_price=product.price * quantity,
>>>>>>> backend
        )
        session.add(new_order)

        # Reduce product stock
        product.order_quantity -= quantity
        session.commit()

        return f"✅ Order placed successfully for {quantity} x {product.product_name} (Size: {size})!"

    except Exception as e:
        session.rollback()
        return f"Order placement error: {e}"

    finally:
        session.close()


<<<<<<< HEAD

@router.get("/orders/me")
async def get_my_orders(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    
=======
@router.get("/orders/me")
async def get_my_orders(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.user_id)
        .all()
    )
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

>>>>>>> backend
    # For constructing the links we use a base URL.
    # In a real router, you might use request.url_for or an environment variable.
    base_url = "http://127.0.0.1:8000"

<<<<<<< HEAD
    
=======
>>>>>>> backend
    orders_with_links = []
    for order in orders:
        order_data = {
            "order_id": order.order_id,
            "user_id": order.user_id,
            "status": order.status,
            # Link to view full order details (e.g., order summary, bill, etc.)
            "order_details_url": f"{base_url}/order/{order.order_id}",
            # Link to view product details for items in this order
<<<<<<< HEAD
            "product_details_url": f"{base_url}/order/{order.order_id}/products"
        }
        orders_with_links.append(order_data)
        print(order_data)
    
    return orders_with_links



@router.get("/orders/{order_id}/bill", response_model=schemas.BillOut)
async def get_bill_for_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
=======
            "product_details_url": f"{base_url}/order/{order.order_id}/products",
        }
        orders_with_links.append(order_data)
        print(order_data)

    return orders_with_links


@router.get("/order/{order_id}/bill", response_model=schemas.BillOut)
async def get_bill_for_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
>>>>>>> backend
    """
    Retrieve the bill information for a given order.
    Ensures the order belongs to the current user.
    """
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.user_id:
<<<<<<< HEAD
        raise HTTPException(status_code=403, detail="You do not have permission to view this order's bill")
=======
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this order's bill",
        )
>>>>>>> backend

    bill = db.query(models.Bill).filter(models.Bill.order_id == order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")
    return bill

<<<<<<< HEAD
  
  
@router.get("/orders/{order_id}/details", response_model=schemas.OrderDetailOut)
async def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get the order ensuring it belongs to the current user
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id,
        models.Order.user_id == current_user.user_id
    ).first()
=======

@router.get("/order/{order_id}/details", response_model=schemas.OrderDetailOut)
async def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Get the order ensuring it belongs to the current user
    order = (
        db.query(models.Order)
        .filter(
            models.Order.order_id == order_id,
            models.Order.user_id == current_user.user_id,
        )
        .first()
    )
>>>>>>> backend
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Get the bill for this order
    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()

    # Retrieve order items with product and brand details.
    # We join OrderItem with Product and then join Product with Brand.
<<<<<<< HEAD
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
=======
    order_items_query = (
        db.query(models.OrderItem, models.Product, models.Brand)
        .join(models.Product, models.OrderItem.product_id == models.Product.product_id)
        .join(models.Brand, models.Product.brand_id == models.Brand.brand_id)
        .filter(models.OrderItem.order_id == order.order_id)
        .all()
    )
>>>>>>> backend

    order_items = []
    for order_item, product, brand in order_items_query:
        item_data = {
            "product_id": product.product_id,
            "brand_id": brand.brand_id,
            "product_name": product.product_name,
            "brand_name": brand.brand_name,
            "order_size": order_item.size,  # assuming OrderItem has a column 'size'
<<<<<<< HEAD
            "order_quantity": order_item.quantity
        }
        
=======
            "order_quantity": order_item.quantity,
        }
<<<<<<< HEAD
        
=======
>>>>>>> 54066bc9f1766879eb45177911b2216d15f00273
>>>>>>> backend
        order_items.append(item_data)

    # Construct the output data
    result = {
        "order_id": order.order_id,
        "status": order.status,
        "created_at": order.created_at,
        "bill_amount": bill.amount if bill else None,
<<<<<<< HEAD
        "order_items": order_items
=======
        "order_items": order_items,
>>>>>>> backend
    }
    return result


<<<<<<< HEAD

@router.get("/orders/me/details", response_model=List[schemas.OrderDetailOut])
async def get_all_order_details(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
=======
@router.get("/orders/me/details", response_model=List[schemas.OrderDetailOut])
async def get_all_order_details(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
>>>>>>> backend
):
    """
    Retrieve all orders for the current user, including:
    - Order id, status, created_at, bill amount
    - A list of order items with product and brand details
    """
<<<<<<< HEAD
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
        
        
=======
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.user_id)
        .all()
    )
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    orders_details = []
    for order in orders:
        # Retrieve the bill for this order
        bill = (
            db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
        )
        # print(bill)
        # Retrieve order items along with product and brand details
        order_items_query = (
            db.query(models.OrderItem, models.Product, models.Brand)
            .join(
                models.Product, models.OrderItem.product_id == models.Product.product_id
            )
            .join(models.Brand, models.Product.brand_id == models.Brand.brand_id)
            .filter(models.OrderItem.order_id == order.order_id)
            .all()
        )
>>>>>>> backend

        order_items = []
        for order_item, product, brand in order_items_query:
            item_data = {
                "product_id": product.product_id,
                "brand_id": brand.brand_id,
                "product_name": product.product_name,
                "brand_name": brand.brand_name,
                "order_size": order_item.size,  # Adjust if your column name is different
<<<<<<< HEAD
                "order_quantity": order_item.quantity
            }
           
            order_items.append(item_data)
            
=======
                "order_quantity": order_item.quantity,
            }
<<<<<<< HEAD
           
            order_items.append(item_data)
            
=======
            order_items.append(item_data)
>>>>>>> 54066bc9f1766879eb45177911b2216d15f00273
>>>>>>> backend

        order_data = {
            "order_id": order.order_id,
            "status": order.status,
            "bill_status": bill.status if bill else None,
            "created_at": order.created_at,
            "bill_amount": bill.amount if bill else None,
<<<<<<< HEAD
            "order_items": order_items
        }
        
        orders_details.append(order_data)
    
    return orders_details


@router.delete("/orders/{order_id}")
async def delete_order(
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
    
=======
            "order_items": order_items,
        }
<<<<<<< HEAD
        
        orders_details.append(order_data)
    
=======
        orders_details.append(order_data)

>>>>>>> 54066bc9f1766879eb45177911b2216d15f00273
    return orders_details


@router.delete("/order/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Retrieve the order ensuring it belongs to the current user
    order = (
        db.query(models.Order)
        .filter(
            models.Order.order_id == order_id,
            models.Order.user_id == current_user.user_id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

>>>>>>> backend
    # Retrieve the associated bill for this order
    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")
<<<<<<< HEAD
    
=======

>>>>>>> backend
    # Check if the bill's status is still "Pending" (case-insensitive)
    if bill.status.lower() != "pending":
        raise HTTPException(
            status_code=400,
<<<<<<< HEAD
            detail="Cannot delete order: bill is already confirmed or processed."
        )
    
    # Delete the order (if cascading is set up, related order items and bill might be deleted automatically)
    db.delete(order)
    db.commit()
    
=======
            detail="Cannot delete order: bill is already confirmed or processed.",
        )

    # Delete the order (if cascading is set up, related order items and bill might be deleted automatically)
    db.delete(order)
    db.commit()

>>>>>>> backend
    return {"detail": "Order deleted successfully."}
