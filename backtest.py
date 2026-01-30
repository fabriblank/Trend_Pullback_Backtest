R_MULTIPLE = 1.25
MAX_WAIT = 8

def backtest(df):
    trades = []
    in_trade = False

    for i in range(30, len(df) - 1):
        row = df.iloc[i]

        if not in_trade:
            if row.trend == 1 and row.valid_pullback:

                for j in range(i + 1, min(i + MAX_WAIT, len(df) - 1)):
                    c = df.iloc[j]

                    trigger = (
                        c.close > c.open and
                        c.close > df.iloc[j - 1].high and
                        (c.high - c.low) > 0.8 * c.ATR
                    )

                    if trigger:
                        entry = c.close
                        stop = row.low - 0.25 * c.ATR
                        risk = entry - stop
                        target = entry + R_MULTIPLE * risk

                        in_trade = True
                        break

        if in_trade:
            c = df.iloc[i]

            if c.low <= stop:
                trades.append(-1.0)
                in_trade = False

            elif c.high >= target:
                trades.append(R_MULTIPLE)
                in_trade = False

    return trades
