import yfinance as yf
import matplotlib.pyplot as plt


## Ambil Data Market
data = yf.download("GC=F", period="1y")
# data1 = yf.download("GC=F", period="2y")

print(data.head())
# print(data1.head())


print("------------------------")


## Hitung Moving Average
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()


## Buat Signal Trading
data['Signal'] = 0

data.loc[data['MA20'] > data['MA50'], 'Signal'] = 1
data.loc[data['MA20'] < data['MA50'], 'Signal'] = -1


# Hitung return market
data['Return'] = data['Close'].pct_change()

# Return strategy
data['Strategy_Return'] = data['Return'] * data['Signal'].shift(1)

# Cumulative return
data['Cumulative_Market'] = (1 + data['Return']).cumprod()
data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod()

## Lihat Hasil Signal
print(data[['Close', 'MA20', 'MA50', 'Signal']].tail(20))


# Plot Chart
plt.figure(figsize=(14,7))

plt.plot(data['Close'], label='Close Price')
plt.plot(data['MA20'], label='MA20')
plt.plot(data['MA50'], label='MA50')
plt.plot(data['Cumulative_Market'], label='Buy & Hold')
plt.plot(data['Cumulative_Strategy'], label='Strategy')

plt.legend()
plt.title('Moving Average Crossover Strategy')

plt.show()