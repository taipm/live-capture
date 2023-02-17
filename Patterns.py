import talib
import pandas as pd
import mplfinance as mpf
from vnstock import *

symbol = 'VND'
df = stock_historical_data(symbol=symbol, start_date='2022-10-01', end_date='2023-02-16')
df['Date'] = df['TradingDate']
del df['TradingDate']
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Lấy dữ liệu giá cổ phiếu
#df = pd.read_csv('stock_prices.csv', index_col='Date', parse_dates=True)

# Tính toán các chỉ báo TA-Lib
df['CDL3INSIDE'] = talib.CDL3INSIDE(df['Open'], df['High'], df['Low'], df['Close'])

# Tạo bộ phận đánh dấu
cdl3inside_mark = mpf.make_addplot(df['CDL3INSIDE'], type='scatter', markersize=100, marker='^', color='r')

# Vẽ đồ thị
mpf.plot(df, type='candle', addplot=[cdl3inside_mark], volume=True, style='charles', title='Stock Prices')

#plt.show()


import ta.volume
import yfinance as yf
import matplotlib.pyplot as plt

# Lấy dữ liệu giá của cổ phiếu Apple
data = df

# Tính toán giá trị của Force Index với độ dài 13
force_index = ta.volume.force_index(close= data['Close'], volume= data['Volume'], window=13, fillna=True)

# Vẽ đồ thị giá và đồ thị Force Index
fig, ax = plt.subplots(2, 1, figsize=(15, 10), sharex=True)

ax[0].plot(data['Close'])
ax[0].set_title(f'Giá đóng cửa {symbol}')
ax[1].plot(force_index)
ax[1].axhline(y=0, color='r', linestyle='-')
ax[1].set_title('Force Index (13)')

plt.show()


import talib
import yfinance as yf
import matplotlib.pyplot as plt

# Lấy dữ liệu giá của cổ phiếu Apple


# Tính toán giá trị của MFI với độ dài 14
mfi = talib.MFI(data['High'], data['Low'], data['Close'], data['Volume'], timeperiod=14)

# Vẽ đồ thị giá và đồ thị MFI
fig, ax = plt.subplots(2, 1, figsize=(15, 10), sharex=True)

ax[0].plot(data['Close'])
ax[0].set_title('Giá đóng cửa')
ax[1].plot(mfi)
ax[1].axhline(y=20, color='r', linestyle='-')
ax[1].axhline(y=80, color='r', linestyle='-')
ax[1].set_title('Money Flow Index (14)')

plt.show()


import yfinance as yf
import pandas as pd
import talib
import ta
import matplotlib.pyplot as plt

class StockChart:
    def __init__(self, symbol):
        self.symbol = symbol
        df = stock_historical_data(symbol=symbol, start_date='2022-10-01', end_date='2023-02-16')
        df['Date'] = df['TradingDate']
        del df['TradingDate']
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        self.data = df# yf.download(symbol, start="2022-01-01", end="2022-02-16")
        self.close = self.data['Close']
        self.open = self.data['Open']
        self.high = self.data['High']
        self.low = self.data['Low']
        self.volume = self.data['Volume']
        
    # def plot_candlestick_chart(self):
    #     fig = plt.figure(figsize=(12,6))
    #     ax = fig.add_subplot(1,1,1)
    #     ax.set_title(f'{self.symbol} Candlestick Chart')
    #     ax.set_xlabel('Date')
    #     ax.set_ylabel('Price')
    #     candlestick = ta.volume.MFIIndicator(self.open, self.high, self.low, self.close)
    #     bullish = candlestick > 0
    #     bearish = candlestick < 0
    #     ax.plot(self.data.index[bullish], self.close[bullish], 'g^', alpha=0.75)
    #     ax.plot(self.data.index[bearish], self.close[bearish], 'rv', alpha=0.75)
    #     ax.grid(True)
    #     ax.xaxis_date()
    #     plt.show()
        
    def plot_vwap(self):
        fig = plt.figure(figsize=(12,6))
        ax = fig.add_subplot(1,1,1)
        ax.set_title(f'{self.symbol} VWAP')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        vwap = ta.volume.VolumePriceTrendIndicator(self.close, self.volume, True)
        ax.plot(self.data.index, vwap, label='VWAP', color='blue')
        ax.plot(self.data.index, self.close, label='Close', color='black')
        ax.legend()
        ax.grid(True)
        ax.xaxis_date()
        plt.show()
        
    def plot_accumulation_distribution(self):
        fig = plt.figure(figsize=(12,6))
        ax = fig.add_subplot(1,1,1)
        ax.set_title(f'{self.symbol} Accumulation/Distribution')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ad = talib.AD(self.high, self.low, self.close, self.volume)
        ax.plot(self.data.index, ad, label='Accumulation/Distribution', color='blue')
        ax.plot(self.data.index, self.close, label='Close', color='black')
        ax.legend()
        ax.grid(True)
        ax.xaxis_date()
        plt.show()

stock = StockChart('ASM')
#stock.plot_candlestick_chart()
stock.plot_vwap()
stock.plot_accumulation_distribution()

