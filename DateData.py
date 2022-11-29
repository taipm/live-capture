from Caculator import *
import numpy as np
from DateHelper import *
from Constant import *
import pandas as pd

class DateData:
    '''
    DỮ LIỆU HÀNG NGÀY
    '''
    def __init__(self, symbol, index, df_all_data) -> None:
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