### Configuration module for environment variables

import os
from dotenv import load_dotenv

### Load variables from .env file if present
load_dotenv()

### Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "appdb")

### Construct the database URL for SQLAlchemy
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

### Application configuration
APP_PORT = int(os.getenv("APP_PORT", 8000))
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() in ("1", "true", "yes")
