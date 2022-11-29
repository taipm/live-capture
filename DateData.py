from Caculator import *
import numpy as np
from DateHelper import *
from Constant import *
import pandas as pd

class DateData:
    '''
    DỮ LIỆU HÀNG NGÀY
    '''
    def __init__(self, symbol, index, df_all_data:pd.DataFrame) -> None:
        self.symbol = symbol.upper()
        self.index = index
        self.df_all_data = df_all_data
        self.data_item = self.df_all_data.iloc[index]
        
        self.date  = self.data_item['Date']
        self.close = self.data_item['Close']
        self.open = self.data_item['Open']
        self.high = self.data_item['High']
        self.low = self.data_item['Low']
        self.volume = self.data_item['Volume']
        self.margin = self.data_item['%']

        self.foriegn_buy = self.data_item['NN Mua']
        self.foriegn_sell = self.data_item['NN Ban']

    @property
    def price(self):
        if self.close > 0:
            return self.close
        else:
            return self.open
    
    def getMA(self, window:int):
        df = self.df_all_data.sort_values(by=['Date'])
        short_rolling = df['Close'].rolling(window=window).mean()
        short_rolling.tail()
        return short_rolling[0]

    def getMaxPrice(self, window:int)->float:
        return np.max(self.df_all_data['Close'][0:window])

    def getMinPrice(self, window:int)->float:
        return np.min(self.df_all_data['Close'][0:window])
    
    def get_distance_price(self, window:int)->float:
        min = self.getMinPrice(window=window)
        max = self.getMaxPrice(window=window)
        if window == 0:
            min = self.low
            max = self.high
        distance = ((max-min)/min)*100
        print(f'{window} : {min} -> {max} = {distance:,.2f}')
        return distance

    @property
    def isSwing(self):
        d = self.get_distance_price(window=0)
        if d >= 7:
            return True
        else:
            return False
    
    @property
    def isSleep(self):
        d = self.get_distance_price(window=0)
        if d <= 3:
            return True
        else:
            return False

    @property
    def isHighest(self):
        if self.high == self.close:
            return True
        else:
            return False

    @property
    def isLowest(self):
        if self.low == self.close:
            return True
        else:
            return False
    @property
    def isFL(self):
        if self.margin <= -6.67:
            return True
        else:
            return False
    @property
    def isGreen(self):
        if self.close >= self.open:
            return True
        else:
            return False
    @property
    def isYELLOW(self):
        if self.close == self.open:
            return True
        else:
            return False

    @property
    def isRED(self):
        if self.close < self.open:
            return True
        else:
            return False

    @property
    def isCE(self):
        if self.margin >= 6.67:
            return True
        else:
            return False

    def analysis(self):
        pass

    def __str__(self) -> str:
        return f'{self.symbol} | {self.price:,.2f}'+\
            f'{self.volume:,.0f}'