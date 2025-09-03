"""Simple auto-trader loop."""
from __future__ import annotations
import time
import threading
import logging
from utils.helpers import get_default_symbols
from trading.scalping_strategy import analyze_scalping_signals
from trading.trade_executor import TradeExecutor

logger = logging.getLogger(__name__)


def trader_loop(stop_event: threading.Event) -> None:
    executor = TradeExecutor()
    symbols = get_default_symbols()
    while not stop_event.is_set():
        for sym in symbols:
            signal = analyze_scalping_signals(sym)
            if signal["signal"] in {"BUY", "SELL"}:
                qty = 0.001  # fixed small qty
                executor.place_market_order(sym, signal["signal"], qty)
        time.sleep(5)


class AutoTrader:
    """Background auto trader."""

    def __init__(self) -> None:
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=trader_loop, args=(self._stop_event,), daemon=True)
        self._thread.start()
        logger.info("AutoTrader started")

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        logger.info("AutoTrader stopped")
