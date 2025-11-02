from dataclasses import dataclass, asdict
import random

@dataclass
class Order:
    id: int
    items: list
    total: float
    status: str

    def to_dict(self):
        """Converts the Order object into a dictionary (for JSON serialization)."""
        return asdict(self)

    @staticmethod
    def create_from_cart(order_id: int, cart, force_status: str | None = None):
        """
        Creates an Order from a shopping cart.
        The payment status is either random ('paid' or 'failed')
        or can be explicitly set via the `force_status` parameter.
        """
        status = force_status or random.choice(["paid", "failed"])
        return Order(
            id=order_id,
            items=cart.to_list(),
            total=cart.get_total_price(),
            status=status
        )
