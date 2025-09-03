"""Reset the SQLite database (development only)."""
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL", "sqlite:///trading_bot.db")
DB_PATH = DB_URL.replace("sqlite:///", "")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("Database removed")
else:
    print("Database not found")
