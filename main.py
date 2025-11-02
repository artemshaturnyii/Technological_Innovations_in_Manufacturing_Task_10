from fastapi import FastAPI, HTTPException, Query
from Warehouse import Warehouse
from Cart import Cart
from Order import Order
import threading

app = FastAPI(title="Minimal Headless Shop")

# --- Data initialization ---
warehouse = Warehouse()
warehouse.load_products_from_json("products.json")

carts = {}   # cart_id → Cart
orders = {}  # order_id → Order
next_order_id = 1


# --- Background task for cleaning up expired carts ---
def cleanup_carts():
    """Periodically removes expired carts from memory."""
    while True:
        expired = [cid for cid, cart in carts.items() if cart.is_expired()]
        for cid in expired:
            del carts[cid]
        threading.Event().wait(60)  # run every 60 seconds


threading.Thread(target=cleanup_carts, daemon=True).start()


# --- API Endpoints ---

@app.get("/products")
def list_products():
    """Returns a list of all available products."""
    return warehouse.to_list()


@app.post("/cart/{cart_id}/add/{product_id}")
def add_to_cart(cart_id: str, product_id: int, quantity: int = 1):
    """Adds a product to a user's cart."""
    if product_id not in warehouse.items:
        raise HTTPException(404, "Product not found")

    if cart_id not in carts:
        carts[cart_id] = Cart()

    cart = carts[cart_id]
    cart.add_product(warehouse.items[product_id]['product'], quantity)
    cart.touch()

    return {"cart": cart.to_list(), "total": cart.get_total_price()}


@app.post("/cart/{cart_id}/remove/{product_id}")
def remove_from_cart(cart_id: str, product_id: int):
    """Removes a product from the user's cart."""
    if cart_id not in carts:
        raise HTTPException(404, "Cart not found")

    cart = carts[cart_id]
    cart.remove_product(product_id)
    cart.touch()

    return {"cart": cart.to_list(), "total": cart.get_total_price()}


@app.post("/cart/{cart_id}/checkout")
def checkout(cart_id: str, status: str | None = Query(None)):
    """
    Performs a checkout operation.
    Randomly sets payment status to 'paid' or 'failed',
    or accepts a fixed status via query parameter (?status=paid).
    """
    global next_order_id

    if cart_id not in carts:
        raise HTTPException(404, "Cart not found")

    cart = carts[cart_id]
    cart.touch()

    # Create the order
    order = Order.create_from_cart(next_order_id, cart, force_status=status)
    orders[next_order_id] = order
    next_order_id += 1

    # Decrease warehouse stock if order was paid
    if order.status == "paid":
        for item in cart.items.values():
            pid = item['product'].id
            warehouse.decrease_inventory(pid, item['quantity'])

    del carts[cart_id]
    return order.to_dict()


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    """Returns an order by its ID."""
    if order_id not in orders:
        raise HTTPException(404, "Order not found")
    return orders[order_id].to_dict()
