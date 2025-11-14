# db/repository.py
from sqlalchemy.orm import Session
from db import models
from typing import List, Dict
from datetime import datetime

def get_products(db: Session, limit: int = 100, offset: int = 0) -> List[models.Product]:
    return db.query(models.Product).offset(offset).limit(limit).all()

def get_product(db: Session, product_id: int) -> models.Product | None:
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def decrease_inventory(db: Session, product_id: int, qty: int) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    if product.quantity < qty:
        return False
    product.quantity -= qty
    db.add(product)
    return True

def create_order_from_cart(db: Session, cart_items: Dict[int, int], force_status: str | None = None):
    """
    cart_items: mapping product_id -> quantity
    Returns created order object
    """
    # Decide status (simulate payment) — you can replace with deterministic logic if force_status supplied
    import random
    status = force_status if force_status in ("paid", "failed") else random.choice(["paid", "failed"])

    # Create order
    order = models.Order(status=status, created_at=datetime.utcnow())
    db.add(order)
    db.flush()  # get order.id

    # Create order items
    items = []
    for pid, qty in cart_items.items():
        product = get_product(db, pid)
        if not product:
            raise ValueError(f"Product {pid} not found")
        oi = models.OrderItem(order_id=order.id, product_id=pid, quantity=qty)
        db.add(oi)
        items.append(oi)
    # do not commit here if transaction managed by caller
    return order
