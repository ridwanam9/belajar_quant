import yfinance as yf
import matplotlib.pyplot as plt


## Ambil Data Market
data = yf.download("GC=F", period="6mo")
# data1 = yf.download("GC=F", period="2y")

print(data.head())
# print(data1.head())


print("------------------------")


ma_j = 20 # garis ema kecil
ma_k = 100 # garis ema besar

## Hitung Moving Average
data[f'MA{ma_j}'] = data['Close'].rolling(window=ma_j).mean()
data[f'MA{ma_k}'] = data['Close'].rolling(window=ma_k).mean()


## Buat Signal Trading
data['Signal'] = 0

data.loc[data[f'MA{ma_j}'] < data[f'MA{ma_k}'], 'Signal'] = -1
data.loc[data[f'MA{ma_j}'] > data[f'MA{ma_k}'], 'Signal'] = 1


# Hitung return market
data['Return'] = data['Close'].pct_change()

# Return strategy
data['Strategy_Return'] = data['Return'] * data['Signal'].shift(1)

# Cumulative return
data['Cumulative_Market'] = (1 + data['Return']).cumprod()
data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod()

## Lihat Hasil Signal
print(data[['Close', f'MA{ma_j}', f'MA{ma_k}', 'Signal']].tail(20))


# Plot Chart
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,7))

# Chart harga
ax1.plot(data['Close'], label='Close Price')
ax1.plot(data[f'MA{ma_j}'], label=f'MA{ma_j}')
ax1.plot(data[f'MA{ma_k}'], label=f'MA{ma_k}')

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