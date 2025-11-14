from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.dependencies import get_db
from db import repository
from Warehouse import Warehouse
from Order import OrderService
import schemas

app = FastAPI(title="Headless Shop API")

# --- Product Endpoints ---
@app.get("/products", response_model=list[schemas.ProductOut])
def list_products(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return repository.get_products(db, limit, offset)

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = repository.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# --- Cart / Order Endpoints ---
@app.post("/orders", response_model=schemas.OrderOut)
def create_order(cart_items: dict[int, int], db: Session = Depends(get_db)):
    warehouse = Warehouse(db)
    # Проверка наличия товара
    for pid, qty in cart_items.items():
        if not warehouse.decrease_inventory(pid, qty):
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {pid}")

    order_service = OrderService(db)
    order = order_service.create_order_from_cart(cart_items)
    return order

# --- Health Check ---
@app.get("/health")
def health(db: Session = Depends(get_db)):
    """
    Проверка подключения к БД.
    Возвращает OK, если соединение работает, иначе FAIL с ошибкой.
    """
    try:
        result = db.execute("SELECT 1").scalar()
        return {"status": "OK", "db_result": result}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}
