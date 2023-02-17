import pprint
import pandas as pd
import matplotlib.pyplot as plt
import talib
import numpy as np
# Tải dữ liệu giá cổ phiếu vào dataframe
import db
df = db.GetStockData(symbol='VGI')
df = df.sort_values(by=['Date'])
#import pandas as pd
import numpy as np
import talib

def best_buy_point(df):
    # Tính MACD và giá trị tín hiệu
    macd, macd_signal, macd_hist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    
    # Tính Bollinger Bands
    upper, middle, lower = talib.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    
    # Tính RSI
    rsi = talib.RSI(df['Close'], timeperiod=14)
    
    # Tính Moving Average
    ma_5 = talib.MA(df['Close'], timeperiod=5, matype=0)
    ma_10 = talib.MA(df['Close'], timeperiod=10, matype=0)
    ma_20 = talib.MA(df['Close'], timeperiod=20, matype=0)
    
    # Xác định điểm mua dựa trên các giá trị trên
    buy_points = []
    for i in range(len(df)):
        if (macd[i] > macd_signal[i] and macd_hist[i] > 0 and
            df['Close'][i] < upper[i] and df['Close'][i] > lower[i] and
            rsi[i] < 50 and 
            ma_5[i] > ma_10[i] and ma_10[i] > ma_20[i]):
            buy_points.append([i,df['Date'][i],df['Close'][i]])
            #buy_points.append([i])
    
    return buy_points

print(best_buy_point(df=df))


import pandas as pd
import ta

# Load dữ liệu cổ phiếu
#df = pd.read_csv('data.csv')

# Áp dụng các kỹ thuật để xác định điểm mua và điểm bán
df = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume", fillna=True)
df['bb_upper'], df['bb_lower'] = ta.volatility.BollingerBands(df['Close'])
df['rsi'] = ta.momentum.RSI(df['Close'])
df['macd'], df['macd_signal'], df['macd_hist'] = ta.trend.MACD(df['Close'])
df['sma50'] = ta.trend.SMA(df['Close'], timeperiod=50)
df['sma200'] = ta.trend.SMA(df['Close'], timeperiod=200)

# Xác định điểm mua
df['buy'] = ((df['Close'] < df['bb_lower']) & (df['rsi'] < 30) & (df['macd'] > df['macd_signal']) & (df['Close'] > df['sma50']) & (df['Close'] > df['sma200']))

# Xác định điểm bán
df['sell'] = ((df['Close'] > df['bb_upper']) & (df['rsi'] > 70) & (df['macd'] < df['macd_signal']))

# Lọc các dòng có điểm mua hoặc điểm bán
df = df[df['buy'] | df['sell']]

# In kết quả
print(df)
