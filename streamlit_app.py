import streamlit as st
import pandas as pd

from trend_logic import compute_trend, detect_pullback
from backtest import backtest
from metrics import performance

st.set_page_config(page_title="Trend Pullback ($ Equity)", layout="centered")

st.title("💵 Trend Pullback — Risk-Based Equity")
st.caption("Starting capital: $3 | Risk per trade: 1%")

file = st.file_uploader("Upload OHLCV CSV", type="csv")

if file:
    df = pd.read_csv(file)

    df = compute_trend(df)
    df = detect_pullback(df)

    trades = backtest(df)
    stats, curve = performance(trades)

    st.subheader("📊 Results")
    st.json(stats)

    st.subheader("📈 Equity Curve ($)")
    st.line_chart(curve.set_index("trade")["equity_usd"])

    st.subheader("📉 Drawdown ($)")
    st.line_chart(curve.set_index("trade")["drawdown_usd"])
