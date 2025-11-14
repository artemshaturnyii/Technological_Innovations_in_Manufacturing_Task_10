# load_products.py
from Warehouse import Warehouse
from db.session import SessionLocal

def main():
    db = SessionLocal()
    w = Warehouse(db)
    w.load_products_from_json("products.json")
    print("✅ Products loaded successfully.")

if __name__ == "__main__":
    main()

