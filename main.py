from fastapi import FastAPI, HTTPException, Query
from Warehouse import Warehouse
from Cart import Cart
from Order import OrderService

app = FastAPI()                     ### FastAPI application instance

warehouse = Warehouse()             ### Warehouse instance for managing products
warehouse.load_products_from_json("products.json")

cart = Cart(ttl_minutes=10)         ### Cart instance with 10-minute inactivity timeout
orders = OrderService()             ### Service for handling orders

@app.get("/products")
async def list_products():
    ### Returns list of all products in warehouse
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "quantity": warehouse.quantities[p.id],
        }
        for p in warehouse.products.values()
    ]

@app.post("/cart/add/{product_id}")
async def add_to_cart(product_id: int, quantity: int = Query(1, gt=0)):
    ### Adds a product to the shopping cart
    if product_id not in warehouse.products:
        raise HTTPException(status_code=404, detail="Product not found")

    available = warehouse.quantities.get(product_id, 0)
    if available < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    product = warehouse.products[product_id]
    cart.add_product(product)
    cart.increase_quantity_product(product_id, quantity - 1)
    cart.touch()                    ### Updates last activity time
    return {"message": f"Added {quantity} of {product.name} to cart"}

@app.post("/cart/remove/{product_id}")
async def remove_from_cart(product_id: int, quantity: int = Query(1, gt=0)):
    ### Removes a product or decreases its quantity in the cart
    if product_id not in cart.products:
        raise HTTPException(status_code=404, detail="Product not in cart")

    cart.decrease_quantity_product(product_id, quantity)
    cart.touch()
    return {"message": f"Removed {quantity} from cart"}

@app.post("/checkout")
async def checkout(force_status: str | None = Query(None)):
    ### Creates an order from the cart and simulates payment
    if cart.is_expired():
        raise HTTPException(status_code=400, detail="Cart expired")

    if not cart.products:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = orders.create_order(cart, force_status=force_status)

    if order.status == "paid":
        for pid, qty in order.items.items():
            warehouse.decrease_inventory(pid, qty)

    cart.__init__()                 ### Clears the cart after checkout
    return order.to_dict()

@app.get("/orders")
async def list_orders():
    ### Returns list of all created orders
    return [o.to_dict() for o in orders.orders.values()]
