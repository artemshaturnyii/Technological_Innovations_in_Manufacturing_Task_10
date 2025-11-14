# Warehouse.py
import json
from db import repository, models
from sqlalchemy.orm import Session

class Warehouse:
    def __init__(self, db: Session):
        self.db = db

    def load_products_from_json(self, path: str):
        """Load products from JSON file into the database"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                products = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {path} not found")

        for prod in products:
            existing = repository.get_product(self.db, prod["id"])
            if existing:
                existing.quantity += prod.get("quantity", 10)
                self.db.add(existing)
            else:
                new_product = models.Product(
                    id=prod["id"],
                    name=prod["name"],
                    price=prod["price"],
                    quantity=prod.get("quantity", 10)
                )
                self.db.add(new_product)

        self.db.commit()

    def decrease_inventory(self, product_id: int, qty: int) -> bool:
        """Decrease product stock using repository logic"""
        return repository.decrease_inventory(self.db, product_id, qty)
