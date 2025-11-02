from Product import Product

class ProductList:
    def __init__(self):
        # id → {'product': Product, 'quantity': int}
        self.items = {}

    def add_product(self, product: Product, quantity: int = 1):
        """Adds a product to the list or increases its quantity."""
        if product.id in self.items:
            self.items[product.id]['quantity'] += quantity
        else:
            self.items[product.id] = {'product': product, 'quantity': quantity}

    def remove_product(self, product_id: int):
        """Removes a product from the list."""
        if product_id in self.items:
            del self.items[product_id]

    def change_quantity(self, product_id: int, delta: int):
        """Changes the product quantity (delta can be negative)."""
        if product_id not in self.items:
            return
        new_qty = self.items[product_id]['quantity'] + delta
        if new_qty <= 0:
            self.remove_product(product_id)
        else:
            self.items[product_id]['quantity'] = new_qty

    def get_total_price(self) -> float:
        """Returns the total price of all products."""
        return sum(item['product'].price * item['quantity'] for item in self.items.values())

    def to_list(self):
        """Returns a list of products as dictionaries (for JSON serialization)."""
        return [
            {
                **item['product'].to_dict(),
                'quantity': item['quantity']
            }
            for item in self.items.values()
        ]
