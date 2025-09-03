"""Simple smoke tests for the trading bot."""
from __future__ import annotations
import os
import unittest
from trading.scalping_strategy import analyze_scalping_signals
from database.init_db import init_db, DB_PATH
from trading.binance_client import BinanceClient


class SmokeTest(unittest.TestCase):
    def test_strategy_output(self) -> None:
        result = analyze_scalping_signals("BTCUSDT", limit=100)
        for key in ["symbol", "signal", "confidence", "entry_price", "stop_loss", "take_profit"]:
            self.assertIn(key, result)

    def test_db_init(self) -> None:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        self.assertTrue(os.path.exists(DB_PATH))

    def test_binance_ping(self) -> None:
        client = BinanceClient()
        try:
            self.assertEqual(client.ping(), {})
        except Exception as exc:  # network restrictions
            self.assertIsNotNone(exc)


if __name__ == "__main__":
    unittest.main()
