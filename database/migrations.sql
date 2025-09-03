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
