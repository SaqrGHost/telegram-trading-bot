"""Simple backtest module."""
from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
import os
from .scalping_strategy import analyze_scalping_signals

SAMPLE_CSV = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_ohlcv.csv")


def run_backtest(symbol: str = "BTCUSDT") -> dict:
    df = pd.read_csv(SAMPLE_CSV)
    signals = []
    for i in range(50, len(df)):
        sub = df.iloc[: i + 1]
        sub.to_csv("_tmp.csv", index=False)
        result = analyze_scalping_signals(symbol, limit=len(sub))
        signals.append(result)
    # naive equity curve
    equity = [1000]
    for sig in signals:
        if sig["signal"] == "BUY":
            equity.append(equity[-1] * (1 + 0.001))
        elif sig["signal"] == "SELL":
            equity.append(equity[-1] * (1 - 0.001))
        else:
            equity.append(equity[-1])
    plt.plot(equity)
    plt.title("Equity curve")
    plt.savefig("equity_curve.png")
    return {"trades": signals, "equity_curve": equity}


if __name__ == "__main__":
    run_backtest()
