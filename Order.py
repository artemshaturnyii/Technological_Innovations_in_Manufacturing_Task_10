from db import repository
from sqlalchemy.orm import Session
from datetime import datetime

class OrderService:
    """
    Service to create and manage orders in the database.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_order_from_cart(self, cart_items: dict[int, int], force_status: str | None = None):
        """
        Create an order from cart items (product_id -> quantity)
        and store it in the database.
        Returns the created order object.
        """
        order = repository.create_order_from_cart(self.db, cart_items, force_status)
        self.db.commit()
        return order
