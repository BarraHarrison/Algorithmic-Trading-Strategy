# Algorithmic Trading Strategy in Python
import datetime as dt 
import matplotlib.pyplot as plt 
import pandas_datareader as web 

plt.style.use("dark_background")

moving_average_1 = 30
moving_average_2 = 100

start = dt.datetime.now() - dt.timedelta(days=365 * 3)
end = dt.datetime.now()

data = web.DataReader("FB", "yahoo", start, end)
data[f"SMA_{moving_average_1}"] = data["Adj Close"].rolling(window=moving_average_1).mean()
data[f"SMA_{moving_average_2}"] = data["Adj Close"].rolling(window=moving_average_2).mean()

data = data.iloc[moving_average_2:]
plt.plot(data["Adj Close"], label="Share Price", color="lightgray")
plt.plot(data[f"SMA_{moving_average_1}"], label=f"SMA_{moving_average_1}", color="orange")
plt.plot(data[f"SMA_{moving_average_2}"], label=f"SMA_{moving_average_2}", color="purple")
plt.legend(loc="upper left")
plt.show()