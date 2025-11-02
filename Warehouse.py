from ProductList import ProductList
from Product import Product
import json
import os

class Warehouse(ProductList):
    def load_products_from_json(self, path: str):
        ### Loads products and their quantities from a JSON file
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} not found")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for prod in data:
            product = Product(
                id=prod["id"],               ### Product ID
                name=prod["name"],           ### Product name
                price=prod["price"]          ### Product price
            )

            self.add_product(product)        ### Add product to warehouse
            self.increase_quantity_product(
                product.id, prod.get("quantity", 10) - 1
            )                               ### Set initial quantity

    def decrease_inventory(self, product_id: int, quantity: int):
        ### Decreases product quantity in stock after a successful order
        self.decrease_quantity_product(product_id, quantity)
