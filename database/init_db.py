"""Initialize the SQLite database."""
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///trading_bot.db")
DB_PATH = DB_URL.replace("sqlite:///", "")

SCHEMA = """
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    side TEXT,
    qty REAL,
    entry_price REAL,
    exit_price REAL,
    stop_loss REAL,
    take_profit REAL,
    status TEXT,
    profit REAL,
    opened_ts INTEGER,
    closed_ts INTEGER,
    raw_order TEXT
);
"""


def init_db() -> None:
    """Create database and tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
