from ProductList import ProductList
from Product import Product
import json
import os

class Warehouse(ProductList):
    def load_products_from_json(self, path: str):
        """Loads products and their quantities from a JSON file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} not found")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for prod in data:
            self.add_product(Product(**prod), quantity=prod.get("quantity", 10))

    def decrease_inventory(self, product_id: int, quantity: int):
        """Decreases product quantity in stock after a successful order."""
        self.change_quantity(product_id, -quantity)
