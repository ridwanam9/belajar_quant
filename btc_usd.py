import yfinance as yf
import matplotlib.pyplot as plt


## Ambil Data Market
data = yf.download("BTC-USD", period="1y")

print(data.head())


print("------------------------")


a = 'MA20'
b = 'MA100'

## Hitung Moving Average
data[a] = data['Close'].rolling(window=20).mean()
data[b] = data['Close'].rolling(window=100).mean()


## Buat Signal Trading
data['Signal'] = 0

data.loc[data[a] < data[b], 'Signal'] = -1
data.loc[data[a] > data[b], 'Signal'] = 1


# Hitung return market
data['Return'] = data['Close'].pct_change()

# Return strategy
data['Strategy_Return'] = data['Return'] * data['Signal'].shift(1)

# Cumulative return
data['Cumulative_Market'] = (1 + data['Return']).cumprod()
data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod()

## Lihat Hasil Signal
print(data[['Close', a, b, 'Signal']].tail(20))


# Plot Chart
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,7))

# Chart harga
ax1.plot(data['Close'], label='Close Price')
ax1.plot(data[a], label=a)
ax1.plot(data[b], label=b)

ax1.set_title('Price & Moving Average')
ax1.legend()

# Chart performa strategy
ax2.plot(data['Cumulative_Market'], label='Buy & Hold')
ax2.plot(data['Cumulative_Strategy'], label='Strategy')

ax2.set_title('Strategy Performance')
ax2.legend()

plt.tight_layout()
plt.show()


# Total return strategy
strategy_return = data['Cumulative_Strategy'].iloc[-1] - 1

# Total return market
market_return = data['Cumulative_Market'].iloc[-1] - 1

print(f"Market Return: {market_return:.2%}")
print(f"Strategy Return: {strategy_return:.2%}")