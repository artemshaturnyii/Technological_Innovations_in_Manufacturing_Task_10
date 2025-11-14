import time
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

load_dotenv()  # обязательно до импорта session

from db.session import engine
from db.models import Base

MAX_RETRIES = 10
SLEEP_SECONDS = 2

def wait_for_db():
    for i in range(MAX_RETRIES):
        try:
            with engine.connect() as conn:
                # Используем text() для "сырых" SQL-запросов
                conn.execute(text("SELECT 1"))
            print("✅ Database is ready")
            return
        except OperationalError:
            print(f"⏳ DB not ready, retrying ({i+1}/{MAX_RETRIES})...")
            time.sleep(SLEEP_SECONDS)
    print("❌ Could not connect to DB after retries")
    exit(1)

def init_db():
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")

if __name__ == "__main__":
    init_db()
