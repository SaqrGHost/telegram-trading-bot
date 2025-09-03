"""Wrapper around binance-connector Spot client."""
from __future__ import annotations
import os
from typing import Any, Dict
import logging
from dotenv import load_dotenv

try:
    from binance.spot import Spot as Client  # type: ignore
except Exception as exc:  # pragma: no cover - fail early if package missing
    raise RuntimeError(
        "binance-connector package is required. Install with 'pip install binance-connector'."
    ) from exc

load_dotenv()
logger = logging.getLogger(__name__)


class BinanceClient:
    """Simple Binance client wrapper."""

    def __init__(self) -> None:
        testnet = os.getenv("BINANCE_TESTNET", "True") == "True"
        key = os.getenv("BINANCE_API_KEY", "")
        secret = os.getenv("BINANCE_API_SECRET", "")
        base_url = "https://testnet.binance.vision" if testnet else None
        self.client = Client(api_key=key, api_secret=secret, base_url=base_url)

    def ping(self) -> Dict[str, Any]:
        """Ping the Binance API."""
        return self.client.ping()

    def get_recent_price(self, symbol: str) -> float:
        data = self.client.ticker_price(symbol)
        return float(data["price"])

    def get_account_balance(self, asset: str = "USDT") -> float:
        data = self.client.account()["balances"]
        for b in data:
            if b["asset"] == asset:
                return float(b["free"])
        return 0.0

    def get_exchange_info(self) -> Dict[str, Any]:
        return self.client.exchange_info()

    def round_qty_to_step(self, symbol: str, qty: float) -> float:
        info = self.get_exchange_info()
        for s in info["symbols"]:
            if s["symbol"] == symbol:
                for f in s["filters"]:
                    if f["filterType"] == "LOT_SIZE":
                        step = float(f["stepSize"])
                        return qty - (qty % step)
        return qty

    def round_price_to_tick(self, symbol: str, price: float) -> float:
        info = self.get_exchange_info()
        for s in info["symbols"]:
            if s["symbol"] == symbol:
                for f in s["filters"]:
                    if f["filterType"] == "PRICE_FILTER":
                        tick = float(f["tickSize"])
                        return price - (price % tick)
        return price
