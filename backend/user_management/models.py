from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DECIMAL,
    ARRAY,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship
from user_management.database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=False, default="customer")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    is_verified = Column(Boolean, default=False)

    brands = relationship("Brand", back_populates="user")

    # Add this relationship for Order
    orders = relationship("Order", back_populates="user")


class Brand(Base):
    __tablename__ = "brand"

    brand_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )
    brand_name = Column(String(255), nullable=False)
    brand_description = Column(Text)
    logo = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="brands")
    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand_id = Column(
        Integer, ForeignKey("brand.brand_id", ondelete="CASCADE"), nullable=False
    )
    product_name = Column(String(255), nullable=False)
    product_pic = Column(ARRAY(Text))  # Array of image storage links
    product_video = Column(ARRAY(Text))  # Array of video storage links
    category = Column(String(100), nullable=False)
    description = Column(Text)
    order_size = Column(String(50))
    order_quantity = Column(Integer, nullable=True)
    quantity_unit = Column(String(50))
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    rating = Column(DECIMAL(3, 2), nullable=True)
    approved = Column(Boolean, default=False)

    brand = relationship("Brand", back_populates="products")


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="orders")
    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    bill = relationship(
        "Bill", back_populates="order", cascade="all, delete-orphan", uselist=False
    )  # One-to-one relationship


class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(
        Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        Integer, ForeignKey("product.product_id", ondelete="CASCADE"), nullable=False
    )
    size = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")


class Bill(Base):
    __tablename__ = "bills"
    bill_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(
        Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False
    )
    amount = Column(DECIMAL(10, 2), nullable=False)
    method = Column(String(50), nullable=False)
    trx_id = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    order = relationship("Order", back_populates="bill")
