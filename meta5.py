import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# connect
mt5.initialize()

symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H1

# ambil 500 candle terakhir
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 500)

# ubah ke dataframe
df = pd.DataFrame(rates)

# convert timestamp
df['time'] = pd.to_datetime(df['time'], unit='s')

print(df.head())

mt5.shutdown()