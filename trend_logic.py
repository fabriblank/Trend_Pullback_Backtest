import numpy as np
from ta.volatility import AverageTrueRange

def compute_trend(df, atr_len=14, trend_window=20):
    df = df.copy()

    df["ret"] = np.log(df["close"] / df["close"].shift(1))

    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=atr_len
    ).average_true_range()

    df["ATR"] = atr

    df["trend_strength"] = df["ret"].rolling(trend_window).sum()
    df["trend_thresh"] = 0.5 * df["ATR"] / df["close"]

    df["trend"] = 0
    df.loc[df["trend_strength"] > df["trend_thresh"], "trend"] = 1
    df.loc[df["trend_strength"] < -df["trend_thresh"], "trend"] = -1

    return df


def detect_pullback(df, lookback=20):
    df = df.copy()

    df["impulse_high"] = df["high"].rolling(lookback).max()
    df["impulse_low"] = df["low"].rolling(lookback).min()

    df["impulse"] = df["impulse_high"] - df["impulse_low"]
    df["retracement"] = (df["impulse_high"] - df["low"]) / df["impulse"]

    df["valid_pullback"] = (
        (df["retracement"] >= 0.20) &
        (df["retracement"] <= 0.38)
    )

    return df
