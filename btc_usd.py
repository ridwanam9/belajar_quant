import yfinance as yf
import matplotlib.pyplot as plt


## Ambil Data Market
data = yf.download("BTC-USD", period="2y")

print(data.head())


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

# Total return strategy
strategy_return = data['Cumulative_Strategy'].iloc[-1] - 1

# Total return market
market_return = data['Cumulative_Market'].iloc[-1] - 1

print(f"Market Return: {market_return:.2%}")
print(f"Strategy Return: {strategy_return:.2%}")


# Hitung rolling maximum
data['Rolling_Max'] = data['Cumulative_Strategy'].cummax()

# Drawdown
data['Drawdown'] = (
    data['Cumulative_Strategy']
    / data['Rolling_Max']
) - 1


# Max drawdown
max_drawdown = data['Drawdown'].min()

print(f"Max Drawdown: {max_drawdown:.2%}")


# Sharpe Ratio
sharpe_ratio = (
    data['Strategy_Return'].mean()
    / data['Strategy_Return'].std()
) * (252 ** 0.5)

print(f"Sharpe Ratio: {sharpe_ratio:.2f}")


# Trade profit/loss
trades = data['Strategy_Return'].dropna()

wins = trades[trades > 0]
losses = trades[trades < 0]

winrate = len(wins) / len(trades)

print(f"Winrate: {winrate:.2%}")

# Detect posisi berubah (Spread)
data['Trade'] = data['Signal'].diff().abs()
spread_cost = 0.0001
data['Strategy_Return_After_Cost'] = (
    data['Strategy_Return']
    - (data['Trade'] * spread_cost)
)
data['Cumulative_Strategy_After_Cost'] = (
    1 + data['Strategy_Return_After_Cost']
).cumprod()

#################### Chart ########################
# Plot Chart
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,6))

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


# Chart Drawdown
plt.figure(figsize=(14,5))

plt.plot(data['Drawdown'])

plt.title('Strategy Drawdown')

plt.show()


# Chart Transaction Cost after spread
plt.figure(figsize=(14,7))

plt.plot(
    data['Cumulative_Strategy'],
    label='Without Cost'
)

plt.plot(
    data['Cumulative_Strategy_After_Cost'],
    label='After Spread Cost'
)

plt.legend()
plt.title('Transaction Cost Impact')

plt.show()