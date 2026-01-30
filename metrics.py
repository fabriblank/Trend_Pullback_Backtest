import numpy as np
import pandas as pd

START_CAPITAL = 3.0      # USD
RISK_PER_TRADE = 0.01    # 1%

def performance(trades):
    equity = START_CAPITAL
    equity_curve = []
    drawdown_curve = []

    peak = equity

    for r in trades:
        risk_amount = equity * RISK_PER_TRADE
        equity += r * risk_amount

        peak = max(peak, equity)
        drawdown = equity - peak

        equity_curve.append(equity)
        drawdown_curve.append(drawdown)

    df_curve = pd.DataFrame({
        "trade": range(1, len(trades) + 1),
        "equity_usd": equity_curve,
        "drawdown_usd": drawdown_curve
    })

    wins = [r for r in trades if r > 0]
    losses = [r for r in trades if r < 0]

    stats = {
        "starting_capital_usd": START_CAPITAL,
        "ending_capital_usd": round(equity, 2),
        "total_trades": len(trades),
        "win_rate_%": round(len(wins) / len(trades) * 100, 2) if trades else 0,
        "expectancy_R": round(np.mean(trades), 3) if trades else 0,
        "max_drawdown_usd": round(min(drawdown_curve), 2) if drawdown_curve else 0
    }

    return stats, df_curve
