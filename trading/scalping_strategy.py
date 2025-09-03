"""Scalping strategy implementation without external TA libs."""
from __future__ import annotations
from typing import Dict, List
import pandas as pd
import os

SAMPLE_CSV = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_ohlcv.csv")


def _load_data(limit: int = 300) -> pd.DataFrame:
    df = pd.read_csv(SAMPLE_CSV).tail(limit).reset_index(drop=True)
    return df


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(length).mean()
    ma_down = down.rolling(length).mean()
    rs = ma_up / ma_down
    return 100 - (100 / (1 + rs))


def bollinger(series: pd.Series, length: int = 20, std: int = 2) -> pd.DataFrame:
    ma = series.rolling(length).mean()
    sd = series.rolling(length).std()
    return pd.DataFrame({"lower": ma - std * sd, "upper": ma + std * sd})


def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, k: int = 14, d: int = 3) -> pd.DataFrame:
    lowest = low.rolling(k).min()
    highest = high.rolling(k).max()
    k_line = 100 * (close - lowest) / (highest - lowest)
    d_line = k_line.rolling(d).mean()
    return pd.DataFrame({"k": k_line, "d": d_line})


def macd(series: pd.Series) -> pd.DataFrame:
    ema12 = ema(series, 12)
    ema26 = ema(series, 26)
    macd_line = ema12 - ema26
    signal = ema(macd_line, 9)
    hist = macd_line - signal
    return pd.DataFrame({"hist": hist})


def atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(length).mean()


def analyze_scalping_signals(symbol: str, intervals: List[str] | None = None, limit: int = 300) -> Dict[str, any]:
    df = _load_data(limit)
    price = df["close"]
    bb = bollinger(price)
    r = rsi(price)
    stoch = stochastic(df["high"], df["low"], price)
    m = macd(price)
    ema50 = ema(price, 50)
    ema200 = ema(price, 200)
    a = atr(df["high"], df["low"], price)
    last = df.index[-1]
    p = price.iloc[last]

    confirmations = []
    if p <= bb["lower"].iloc[last]:
        confirmations.append("bollinger_long")
    if p >= bb["upper"].iloc[last]:
        confirmations.append("bollinger_short")
    if r.iloc[last] < 35:
        confirmations.append("rsi_long")
    if r.iloc[last] > 65:
        confirmations.append("rsi_short")
    if stoch["k"].iloc[last] < stoch["d"].iloc[last]:
        confirmations.append("stoch_long")
    else:
        confirmations.append("stoch_short")
    if m["hist"].iloc[last] > 0:
        confirmations.append("macd_long")
    else:
        confirmations.append("macd_short")

    long_conf = len([c for c in confirmations if c.endswith("long")])
    short_conf = len([c for c in confirmations if c.endswith("short")])

    signal = "HOLD"
    position_side = None
    reasons: List[str] = []
    if long_conf >= 3 and p > ema200.iloc[last] and ema50.diff().iloc[-1] > 0:
        signal = "BUY"
        position_side = "LONG"
        reasons.append(">=3 long confirmations")
    elif short_conf >= 3 and p < ema200.iloc[last] and ema50.diff().iloc[-1] < 0:
        signal = "SELL"
        position_side = "SHORT"
        reasons.append(">=3 short confirmations")

    risk = float(a.iloc[last] * 1.5)
    entry_price = p
    stop_loss = entry_price - risk if signal == "BUY" else entry_price + risk
    take_profit = entry_price + 2 * risk if signal == "BUY" else entry_price - 2 * risk

    result = {
        "symbol": symbol,
        "signal": signal,
        "confidence": int(max(long_conf, short_conf) / 5 * 100),
        "entry_price": float(entry_price),
        "stop_loss": float(stop_loss),
        "take_profit": float(take_profit),
        "position_side": position_side,
        "reasons": reasons,
        "indicators": {"rsi": float(r.iloc[last]), "atr": float(a.iloc[last])},
        "sr_levels": [],
        "timestamp": int(df.loc[last, "timestamp"]),
    }
    return result
