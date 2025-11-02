from ProductList import ProductList
import time

class Cart(ProductList):
    def __init__(self, ttl_minutes: int = 10):
        ### Initializes a shopping cart with a time-to-live (TTL) in minutes
        super().__init__()
        self.ttl = ttl_minutes * 60        ### Time-to-live in seconds
        self.last_access = time.time()     ### Last time the cart was accessed

    def touch(self):
        ### Updates the last access time (called on any user activity)
        self.last_access = time.time()

    def is_expired(self) -> bool:
        ### Checks whether the cart has expired based on inactivity
        return (time.time() - self.last_access) > self.ttl
