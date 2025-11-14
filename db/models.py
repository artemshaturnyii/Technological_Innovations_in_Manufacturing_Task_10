### SQLAlchemy models for the headless shop

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

### Base class for all models
Base = declarative_base()

### Product model
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=10, nullable=False)

    ### Optional: string representation
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})>"

### Order model
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="failed", nullable=False)  ### paid / failed
    created_at = Column(DateTime, default=datetime.utcnow)

    ### Relation to order items
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

### OrderItem model
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
