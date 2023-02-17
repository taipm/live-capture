import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split    
from sklearn.metrics import mean_squared_error

# Load dữ liệu chứng khoán
#df = pd.read_csv("stock_data.csv")
import db

# print(df.dtypes)
# df = df.drop("Stock", axis=1)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib

def stock_price_forecast(data):
    close_price = data['Close']
    
    # Calculating Moving Averages
    fast_ma = talib.SMA(close_price, timeperiod=12)
    slow_ma = talib.SMA(close_price, timeperiod=26)

    # Bollinger Bands
    upper_band, middle_band, lower_band = talib.BBANDS(close_price, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    # Relative Strength Index
    rsi = talib.RSI(close_price, timeperiod=14)

    # # Plotting the data
    # fig, ax = plt.subplots(figsize=(15,7))
    # ax.plot(close_price, label='Close Price')
    # ax.plot(fast_ma, label='Fast Moving Average', linestyle='--')
    # ax.plot(slow_ma, label='Slow Moving Average', linestyle='--')
    # ax.plot(upper_band, label='Upper Band', linestyle='--')
    # ax.plot(lower_band, label='Lower Band', linestyle='--')
    # ax.legend(loc='best')
    # plt.show()

    # fig, ax = plt.subplots(figsize=(15,7))
    # ax.plot(rsi, label='Relative Strength Index', color='red')
    # ax.legend(loc='best')
    # plt.show()

    # Based on the Moving Averages and Bollinger Bands, we can make a decision on the stock trend
    output = f'{close_price[0]} - {df["Date"][0]} - rsi: {rsi[0]:,.2f}'
    if fast_ma[0] > slow_ma[0] and close_price[0] > upper_band[0]:
        return output + ": " +  "Sell"
    elif fast_ma[0] < slow_ma[0] and close_price[0] < lower_band[0]:
        return output + ": " +  "Buy"
    elif rsi[0] > 70:
        return output + ": " +  "Sell"
    elif rsi[0] < 30:
        return output + ": " +  "Buy"
    else:
        return output + ": " +  "Hold"

# Importing the dataset
#data = pd.read_csv("stock_data.csv")

symbols = ['VND','HAX','BSI','DGC','FTS','HBC','DXG','SCR', 'BSR','NVL','PDR','VGI','MWG','TPB','VCB','BID','VIB']
for symbol in symbols:
    df = db.GetStockData(symbol=symbol)
    # Forecasting the stock trend
    trend = stock_price_forecast(df)
    print(f"The trend for the stock {symbol} is: {trend}")

