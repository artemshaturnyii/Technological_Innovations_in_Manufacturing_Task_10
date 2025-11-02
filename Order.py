import random
from dataclasses import dataclass, asdict

@dataclass
class Order:
    id: int                  ### Unique order identifier
    items: dict              ### Dictionary: product_id → quantity
    total: float             ### Total order amount
    status: str              ### Payment status ("paid" or "failed")

    def to_dict(self):
        ### Converts Order dataclass to dictionary
        return asdict(self)

class OrderService:
    def __init__(self):
        self.orders = {}     ### Stores all created orders (id → Order)
        self.counter = 1     ### Order ID counter

    def create_order(self, cart, force_status: str | None = None):
        ### Creates an order from cart contents and simulates payment
        items = cart.products.copy()
        quantities = cart.quantities.copy()

        total = sum(
            items[pid].price * quantities[pid] for pid in items
        )                    ### Calculates total cost

        status = (
            force_status if force_status in ["paid", "failed"]
            else random.choice(["paid", "failed"])
        )                    ### Determines payment result (manual or random)

        order = Order(
            id=self.counter,
            items={pid: quantities[pid] for pid in items},
            total=total,
            status=status
        )

        self.orders[self.counter] = order
        self.counter += 1

        return order
