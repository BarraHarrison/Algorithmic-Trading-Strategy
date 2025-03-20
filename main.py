# Algorithmic Trading Strategy in Python
import datetime as dt 
import matplotlib.pyplot as plt 
import yfinance as yf 

plt.style.use("dark_background")

moving_average_1 = 30
moving_average_2 = 100

start = dt.datetime.now() - dt.timedelta(days=365 * 3)
end = dt.datetime.now()

data = yf.download("TSLA", start=start, end=end, auto_adjust=False)

print(data.columns)

if "Adj Close" in data.columns:
    data[f"SMA_{moving_average_1}"] = data["Adj Close"].rolling(window=moving_average_1).mean()
    data[f"SMA_{moving_average_2}"] = data["Adj Close"].rolling(window=moving_average_2).mean()

    data = data.iloc[moving_average_2:]
    plt.figure(figsize=(12, 6))
    plt.plot(data["Adj Close"], label="Share Price", color="lightgray")
    plt.plot(data[f"SMA_{moving_average_1}"], label=f"SMA_{moving_average_1}", color="orange")
    plt.plot(data[f"SMA_{moving_average_2}"], label=f"SMA_{moving_average_2}", color="purple")
    plt.legend(loc="upper left")
    plt.show()
else:
    print("Error: 'Adj Close' column not found in the downloaded data.")


buy_signals = []
sell_signals = []
trigger = 0

for x in range(len(data)):
    if data[f"SMA_{moving_average_1}"].iloc[x] > data[f"SMA_{moving_average_2}"].iloc[x] and trigger != 1:
            buy_signals.append(data["Adj Close"].iloc[x])
            sell_signals.append(float("nan"))
            trigger = 1
    elif data[f"SMA_{moving_average_1}"].iloc[x] < data[f"SMA_{moving_average_2}"].iloc[x] and trigger != -1:
            buy_signals.append(float("nan"))
            sell_signals.append(data["Adj Close"].iloc[x])
            trigger = -1
    else:
         buy_signals.append(float("nan"))
         sell_signals.append(float("nan"))

data["Buy Signals"] = buy_signals
data["Sell Signals"] = sell_signals

print(data)

plt.figure(figsize=(12, 6))
plt.plot(data["Adj Close"], label="Share Price", alpha=0.5)
plt.plot(data[f"SMA_{moving_average_1}"], label=f"SMA_{moving_average_1}", color="orange", linestyle="--")
plt.plot(data[f"SMA_{moving_average_2}"], label=f"SMA_{moving_average_2}", color="pink", linestyle="--")
plt.scatter(data.index, data["Buy Signals"], label="Buy Signal", marker="^", color="lime", linewidths=3)
plt.scatter(data.index, data["Sell Signals"], label="Sell Signal", marker="v", color="red", linewidths=3)
plt.legend(loc="upper left")
plt.show()