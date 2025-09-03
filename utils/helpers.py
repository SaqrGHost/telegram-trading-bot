"""Helper utilities."""
from __future__ import annotations
import os
from decimal import Decimal
from typing import List
from dotenv import load_dotenv

load_dotenv()


def get_authorized_ids() -> List[int]:
    ids = os.getenv("AUTHORIZED_USER_IDS", "")
    return [int(i) for i in ids.split(",") if i.strip()]


def get_default_symbols() -> List[str]:
    symbols = os.getenv("DEFAULT_SYMBOLS", "BTCUSDT").split(",")
    return [s.strip().upper() for s in symbols]


def compute_risk_amount(balance: float) -> float:
    risk = float(os.getenv("RISK_PER_TRADE", 0))
    if risk:
        return balance * risk
    return float(os.getenv("DEFAULT_QUANTITY_USDT", 10))
