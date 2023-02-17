# import talib

# class TrendDetector:
#     def __init__(self, close, timeperiod=14, ma_periods=[10, 20, 50, 100], bb_period=20, bb_stddev=2):
#         self.close = close
#         self.rsi = talib.RSI(close, timeperiod=timeperiod)
#         self.ma10 = talib.SMA(close, timeperiod=ma_periods[0])
#         self.ma20 = talib.SMA(close, timeperiod=ma_periods[1])
#         self.ma50 = talib.SMA(close, timeperiod=ma_periods[2])
#         self.ma100 = talib.SMA(close, timeperiod=ma_periods[3])
#         self.upper, self.middle, self.lower = talib.BBANDS(close, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev)

#     def is_trend_up(self):
#         last_index = -1
#         return self.close[last_index] > self.ma10[last_index] and self.close[last_index] > self.ma20[last_index] and self.close[last_index] > self.ma50[last_index] and self.close[last_index] > self.ma100[last_index] and self.rsi[last_index] > 50 and self.close[last_index] > self.lower[last_index]

# import talib

# class TrendDetector:
#     #def __init__(self, close, timeperiod=14, ma_periods=[10, 20, 50, 100], bb_period=20, bb_stddev=2):
#     def __init__(self, symbol):
#         df = stock_historical_data(symbol=symbol, start_date='2022-10-01', end_date='2023-02-16')
#         df['Date'] = df['TradingDate']
#         del df['TradingDate']
#         df['Date'] = pd.to_datetime(df['Date'])
#         df.set_index('Date', inplace=True)
        

#         close = df['Close'].values
#         high = df['High'].values
#         low = df['Low'].values

#         timeperiod=14
#         ma_periods=[10, 20, 50, 100]
#         bb_period=20
#         bb_stddev=2

#         self.data = df

#         self.close = close
#         self.rsi = talib.RSI(close, timeperiod=timeperiod)
#         self.ma10 = talib.SMA(close, timeperiod=ma_periods[0])
#         self.ma20 = talib.SMA(close, timeperiod=ma_periods[1])
#         self.ma50 = talib.SMA(close, timeperiod=ma_periods[2])
#         self.ma100 = talib.SMA(close, timeperiod=ma_periods[3])
#         self.ema21 = talib.EMA(close, timeperiod=21)
#         self.upper, self.middle, self.lower = talib.BBANDS(close, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev)
#         self.adx = talib.ADX(high, low, close, timeperiod=14)

#     def is_up_trend(self):
#         #return self.close[-1] > self.ma10[-1] and self.close[-1] > self.ma20[-1] and self.close[-1] > self.ma100[-1] and self.rsi[-1] > 50 and self.close[-1] > self.lower[-1] and self.close[-1] > self.ema21[-1]
#         return self.close[-1] > self.ma10[-1] and self.rsi[-1] > 50 and self.close[-1] > self.lower[-1] and self.close[-1] > self.ema21[-1]

#     def is_can_buy(self):
#         last_rsi = self.rsi[-1]
#         ema21 = self.ema21[-1]
#         adx = self.adx[-1]
        

#         if self.is_up_trend() and last_rsi > 50 and last_rsi < 70 and ema21 < self.close[-1] and adx > 25:
#             return True
#         else:
#             return False

#     def is_can_buy_with_volatility(self):
#         stock_data = self.data
#         atr = self.indicators.atr(stock_data)
#         bb_upper, bb_middle, bb_lower = self.indicators.bollinger_bands(stock_data)

#         if stock_data[-1]['Close'] < bb_lower[-1] and stock_data[-1]['Volume'] > atr[-1]:
#             return True
#         else:
#             return False


import talib

class TrendDetector:
    def __init__(self, symbol):
        df = stock_historical_data(symbol=symbol, start_date='2022-10-01', end_date='2023-02-16')
        df['Date'] = df['TradingDate']
        del df['TradingDate']
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        

        close = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        volume = df['Volume'].values

        timeperiod=14
        ma_periods=[10, 20, 50, 100]
        bb_period=20
        bb_stddev=2

        self.data = df

        self.close = close
        self.rsi = talib.RSI(close, timeperiod=timeperiod)
        self.ma10 = talib.SMA(close, timeperiod=ma_periods[0])
        self.ma20 = talib.SMA(close, timeperiod=ma_periods[1])
        self.ma50 = talib.SMA(close, timeperiod=ma_periods[2])
        self.ma100 = talib.SMA(close, timeperiod=ma_periods[3])
        self.ema21 = talib.EMA(close, timeperiod=21)
        self.upper, self.middle, self.lower = talib.BBANDS(close, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev)
        self.adx = talib.ADX(high, low, close, timeperiod=14)
        self.atr = talib.ATR(high, low, close, timeperiod=14)
        self.volume = volume
        self.vwap = talib.VWAP(high, low, close, volume)
        self.typical_price = talib.TYPPRICE(high, low, close)

    def is_up_trend(self):
        return self.close[-1] > self.ma10[-1] and self.rsi[-1] > 50 and self.close[-1] > self.lower[-1] and self.close[-1] > self.ema21[-1]

    def is_can_buy_with_volatility(self):
        last_rsi = self.rsi[-1]
        ema21 = self.ema21[-1]
        adx = self.adx[-1]
        atr = self.atr[-1]
        vwap = self.vwap[-1]
        tp = self.typical_price[-1]

        if self.is_up_trend() and last_rsi > 50 and last_rsi < 70 and ema21 < self.close[-1] and adx > 25:
            if vwap > tp and self.volume[-1] > 1.5 * talib.SMA(self.volume, timeperiod=14)[-1] and self.close[-1] - vwap > 0.5 * atr:
                return True
            else:
                return False
        else:
            return False


# Chuẩn bị dữ liệu đầu vào
from vnstock import *
import pandas as pd

def trendOf(symbol):
    
    # # Tạo đối tượng TrendDetector
    trend_detector = TrendDetector(symbol=symbol)

    # Kiểm tra điều kiện xu hướng tăng
    trend_up = False    
    if trend_detector.is_up_trend():
        #print("Xu hướng tăng")
        trend_up = True

    can_buy = False
    if trend_detector.is_can_buy():
        #print("Xu hướng tăng")
        can_buy = True
    # else:
    #     print("Không có xu hướng tăng")    
    print(f'{symbol} - Xu hướng: {trend_detector.is_up_trend()} : Điểm mua : {trend_detector.is_can_buy()}')
    #return result


symbols = ['IDC','VND','HAX','IJC']
for s in symbols:
    print(f'{s} - {trendOf(symbol=s)}')