
import pandas as pd
from datetime import datetime
from vnstock import *
from ta.trend import ADXIndicator

start_date = '2022-01-01'
symbol = 'HHV'
today_str = datetime.now().strftime("%Y-%m-%d")

df = stock_historical_data(symbol=symbol, start_date=start_date, end_date=today_str)
df['Date'] = df['TradingDate']
del df['TradingDate']
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

n = 14
dmi = ADXIndicator(df['High'], df['Low'], df['Close'], window=n, fillna=False)

result = pd.DataFrame({
    '+DI': dmi.adx_neg(),
    '-DI': dmi.adx_pos(),
    'ADX': dmi.adx()
})

print(result.tail())

import pandas as pd
from datetime import datetime
from vnstock import *
from ta.trend import ADXIndicator
import mplfinance as mpf

start_date = '2022-01-01'
symbol = 'HHV'
today_str = datetime.now().strftime("%Y-%m-%d")

df = stock_historical_data(symbol=symbol, start_date=start_date, end_date=today_str)
df['Date'] = df['TradingDate']
del df['TradingDate']
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

n = 14
dmi = ADXIndicator(df['High'], df['Low'], df['Close'], window=n, fillna=False)

result = pd.DataFrame({
    '+DI': dmi.adx_neg(),
    '-DI': dmi.adx_pos(),
    'ADX': dmi.adx()
})

print(result.tail())

# Plot candlestick chart with ADX indicator
mpf.plot(df, type='candle', style='charles', title=f'{symbol} Candlestick Chart with ADX Indicator',
         ylabel='Price', ylabel_lower='Volume', volume=True, addplot=[mpf.make_addplot(result['ADX']),
                                                                        mpf.make_addplot(result['+DI']),
                                                                        mpf.make_addplot(result['-DI']),],
         figratio=(16, 8), figsize=(16, 8))


import pandas as pd
import mplfinance as mpf
from datetime import datetime
from vnstock import *
from ta.trend import ADXIndicator
import ta
import matplotlib.pyplot as plt

start_date = '2022-01-01'
symbol = 'HHV'
today_str = datetime.now().strftime("%Y-%m-%d")

df = stock_historical_data(symbol=symbol, start_date=start_date, end_date=today_str)
df['Date'] = df['TradingDate']
del df['TradingDate']
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

n = 14
dmi = ADXIndicator(df['High'], df['Low'], df['Close'], window=n, fillna=False)

result = pd.DataFrame({
    '+DI': dmi.adx_neg(),
    '-DI': dmi.adx_pos(),
    'ADX': dmi.adx()
})

ap = [
    mpf.make_addplot(result['+DI'], color='g', panel=1),
    mpf.make_addplot(result['-DI'], color='r', panel=1),
    mpf.make_addplot(result['ADX'], color='b', panel=2)
]

mpf.plot(df, type='candle', style='yahoo', addplot=ap)
plt.show()

