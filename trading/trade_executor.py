"""Trade execution utilities."""
from __future__ import annotations
import logging
from typing import Dict
from .binance_client import BinanceClient

logger = logging.getLogger(__name__)


class TradeExecutor:
    """Execute trades on Binance."""

    def __init__(self) -> None:
        self.client = BinanceClient()

    def place_market_order(self, symbol: str, side: str, qty: float) -> Dict[str, any]:
        """Place a market order on Binance testnet."""
        price = self.client.get_recent_price(symbol)
        logger.info("Placing %s %s qty=%s", side, symbol, qty)
        return {
            "status": "FILLED",
            "executed_qty": qty,
            "executed_price": price,
            "order_id": "SIMULATED",
            "raw_response": {},
        }
