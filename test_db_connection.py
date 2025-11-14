from db.session import engine
from sqlalchemy import text

### Simple connection test
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("✅ Connected to PostgreSQL")
        print(result.fetchone())
except Exception as e:
    print("❌ Connection failed:", e)
