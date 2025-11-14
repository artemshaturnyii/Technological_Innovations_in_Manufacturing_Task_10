# schemas.py
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# --- Product schema ---
class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

    model_config = {
        "from_attributes": True  # Pydantic v2 заменяет orm_mode
    }

# --- OrderItem schema ---
class OrderItemOut(BaseModel):
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }

# --- Order schema ---
class OrderOut(BaseModel):
    id: int
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    model_config = {
        "from_attributes": True
    }

# --- Optional: Cart input schema ---
class CartAddItemIn(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")

    model_config = {
        "from_attributes": True
    }

class CartRemoveItemIn(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")

    model_config = {
        "from_attributes": True
    }
