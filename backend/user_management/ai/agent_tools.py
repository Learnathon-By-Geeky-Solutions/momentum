from langchain_core.tools import tool
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Dict, Any, Optional
from models import Product, Order, OrderItem, Bill
from schemas import OrderCreate, OrderItemCreate, BillCreate
from database import get_db
import re

class AgentTools:
    def __init__(self, db: Session):
        self.db = db

    @tool(name="search_products")
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for products in the database based on a query string.
        The query should describe what the user is looking for.
        
        Args:
            query: A string describing the product(s) to search for
            
        Returns:
            A list of products that match the search criteria
        """
        if not query or not isinstance(query, str):
            return []
            
        # Extract key terms from the query
        search_terms = re.findall(r'\w+', query.lower())
        
        # Filter out common words
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'for', 'want', 'looking', 'need'}
        search_terms = [term for term in search_terms if term not in stop_words and len(term) > 2]
        
        if not search_terms:
            return []
        
        # Construct the search query using SQLAlchemy
        search_filters = []
        for term in search_terms:
            search_filters.append(Product.product_name.ilike(f'%{term}%'))
            search_filters.append(Product.category.ilike(f'%{term}%'))
            search_filters.append(Product.description.ilike(f'%{term}%'))
        
        # Execute the query
        products = self.db.query(Product).filter(
            or_(*search_filters),
            Product.approved == True
        ).limit(10).all()
        
        # Format the results
        results = []
        for product in products:
            results.append({
                "product_id": product.product_id,
                "product_name": product.product_name,
                "brand_id": product.brand_id,
                "category": product.category,
                "description": product.description,
                "price": float(product.price),
                "order_size": product.order_size,
                "quantity_unit": product.quantity_unit,
                "rating": float(product.rating) if product.rating else None
            })
        
        return results

    @tool
    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific product by its ID.
        
        Args:
            product_id: The ID of the product to retrieve
            
        Returns:
            Detailed information about the product
        """
        product = self.db.query(Product).filter(
            Product.product_id == product_id,
            Product.approved == True
        ).first()
        
        if not product:
            return {"error": f"Product with ID {product_id} not found"}
        
        return {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "brand_id": product.brand_id,
            "category": product.category,
            "description": product.description,
            "price": float(product.price),
            "order_size": product.order_size,
            "order_quantity": product.order_quantity,
            "quantity_unit": product.quantity_unit,
            "rating": float(product.rating) if product.rating else None,
            "product_pic": product.product_pic,
            "product_video": product.product_video
        }

    @tool
    def create_order(self, user_id: int, product_id: int, quantity: int, size: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new order for a product.
        
        Args:
            user_id: The ID of the user placing the order
            product_id: The ID of the product being ordered
            quantity: The quantity of the product being ordered
            size: Optional size selection for the product
            
        Returns:
            Information about the created order
        """
        # Check if product exists
        product = self.db.query(Product).filter(
            Product.product_id == product_id,
            Product.approved == True
        ).first()
        
        if not product:
            return {"error": f"Product with ID {product_id} not found"}
        
        # Create a new order
        new_order = Order(
            user_id=user_id,
            status="pending"
        )
        self.db.add(new_order)
        self.db.flush()
        
        # Create order item
        order_item = OrderItem(
            order_id=new_order.order_id,
            product_id=product_id,
            quantity=quantity,
            size=size
        )
        self.db.add(order_item)
        
        # Calculate the total amount
        total_amount = float(product.price) * quantity
        
        # Create a bill with pending status
        bill = Bill(
            order_id=new_order.order_id,
            amount=total_amount,
            method="pending",
            trx_id="pending",
            status="pending"
        )
        self.db.add(bill)
        
        self.db.commit()
        
        return {
            "order_id": new_order.order_id,
            "product_name": product.product_name,
            "quantity": quantity,
            "size": size,
            "total_amount": total_amount,
            "status": new_order.status
        }