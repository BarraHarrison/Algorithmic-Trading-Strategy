# Algorithmic Trading Strategy Using EMA in Python
import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

plt.style.use("dark_background")

TICKER = "NVDA"
EMA_SHORT = 30
EMA_LONG = 100
LOOKBACK_YEARS = 3

def fetch_data(ticker, years):
    start = dt.datetime.now() - dt.timedelta(days=365 * years)
    end = dt.datetime.now()
    data = yf.download(ticker, start=start, end=end, auto_adjust=False)

    # Flatten multi-index columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)

    return data

def calculate_emas(data, short, long):
    data[f"EMA_{short}"] = data["Adj Close"].ewm(span=short, adjust=False).mean()
    data[f"EMA_{long}"] = data["Adj Close"].ewm(span=long, adjust=False).mean()
    return data.iloc[long:]  

def generate_signals(data, short, long):
    buy_signals, sell_signals = [], []
    trigger = 0

    for i in range(len(data)):
        ema_short = data[f"EMA_{short}"].iloc[i]
        ema_long = data[f"EMA_{long}"].iloc[i]
        close_price = data["Adj Close"].iloc[i]

        if ema_short > ema_long and trigger != 1:
            buy_signals.append(close_price)
            sell_signals.append(float("nan"))
            trigger = 1
        elif ema_short < ema_long and trigger != -1:
            buy_signals.append(float("nan"))
            sell_signals.append(close_price)
            trigger = -1
        else:
            buy_signals.append(float("nan"))
            sell_signals.append(float("nan"))

    data["Buy Signals"] = buy_signals
    data["Sell Signals"] = sell_signals
    return data


def plot_emas(data, short, long):
    plt.figure(figsize=(12, 6))
    plt.plot(data["Adj Close"], label="Share Price", color="lightgray")
    plt.plot(data[f"EMA_{short}"], label=f"EMA_{short}", color="orange")
    plt.plot(data[f"EMA_{long}"], label=f"EMA_{long}", color="purple")
    plt.title(f"{TICKER} Price with EMA Crossovers")
    plt.legend(loc="upper left")
    plt.show()

def plot_signals(data, short, long):
    plt.figure(figsize=(12, 6))
    plt.plot(data["Adj Close"], label="Share Price", alpha=0.5)
    plt.plot(data[f"EMA_{short}"], label=f"EMA_{short}", color="orange", linestyle="--")
    plt.plot(data[f"EMA_{long}"], label=f"EMA_{long}", color="pink", linestyle="--")
    plt.scatter(data.index, data["Buy Signals"], label="Buy Signal", marker="^", color="lime", linewidths=3)
    plt.scatter(data.index, data["Sell Signals"], label="Sell Signal", marker="v", color="red", linewidths=3)
    plt.title(f"{TICKER} Trading Signals")
    plt.legend(loc="upper left")
    plt.show()

def main():
    data = fetch_data(TICKER, LOOKBACK_YEARS)

    if "Adj Close" not in data.columns:
        print("Error: 'Adj Close' column not found.")
        return

    data = calculate_emas(data, EMA_SHORT, EMA_LONG)
    data = generate_signals(data, EMA_SHORT, EMA_LONG)

    print(data.tail())

    plot_emas(data, EMA_SHORT, EMA_LONG)
    plot_signals(data, EMA_SHORT, EMA_LONG)

    signal_data = data[
        data["Buy Signals"].notna() | data["Sell Signals"].notna()
    ]

    columns_to_export = ["Adj Close", f"EMA_{EMA_SHORT}", f"EMA_{EMA_LONG}", "Buy Signals", "Sell Signals"]
    signal_data = signal_data[columns_to_export]

    filename = f"{TICKER}_signals_only.csv"
    signal_data.to_csv(filename)
    print(f"📁 Exported buy/sell signals to {filename}")


if __name__ == "__main__":
    main()
