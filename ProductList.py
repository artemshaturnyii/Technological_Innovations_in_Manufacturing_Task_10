from Product import Product

class ProductList:
    def __init__(self):
        self.products = {}      ### Key — product ID, value — Product object
        self.quantities = {}    ### Key — product ID, value — available quantity

    def add_product(self, product: Product):
        ### Adds product to list and sets quantity = 1 if not yet added
        if product.id not in self.products:
            self.products[product.id] = product
            self.quantities[product.id] = 1

    def increase_quantity_product(self, product_id: int, increase_number: int = 1):
        ### Increases quantity of a product by a given number
        if product_id in self.products:
            if increase_number < 0:
                increase_number = 0          ### Prevent negative increment
            self.quantities[product_id] += increase_number

    def decrease_quantity_product(self, product_id: int, decrease_number: int = 1):
        ### Decreases quantity of a product by a given number, not below 0
        if product_id in self.products:
            available_quantity = self.quantities[product_id]
            if decrease_number > available_quantity:
                decrease_number = available_quantity   ### Prevent negative result
            self.quantities[product_id] -= decrease_number
            if self.quantities[product_id] == 0:
                self.remove_product(product_id)

    def remove_product(self, product_id: int):
        ### Removes product from the list
        if product_id in self.products:
            del self.products[product_id]
            del self.quantities[product_id]
