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


## Lihat Hasil Signal
print(data[['Close', 'MA20', 'MA50', 'Signal']].tail(20))


# Plot Chart
plt.figure(figsize=(14,7))

plt.plot(data['Close'], label='Close Price')
plt.plot(data['MA20'], label='MA20')
plt.plot(data['MA50'], label='MA50')

plt.legend()
plt.title('Moving Average Crossover Strategy')

plt.show()