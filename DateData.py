from time import sleep
from Caculator import *
import numpy as np
from DateHelper import *
from Constant import *
import pandas as pd
from RangeMA import RangeMA

class DateData:
    '''
    DỮ LIỆU HÀNG NGÀY
    '''
    def __init__(self, symbol, index:int, df_all_data:pd.DataFrame) -> None:
        self.symbol = symbol.upper()
        self.index = index
        self.df_all_data = df_all_data
        #self.data_item = self.df_all_data.iloc[index]
        self.data_item = self.df_all_data[self.df_all_data.index==index]
        
        self.date  = self.data_item['Date']
        self.close = float(self.data_item['Close'])
        self.open = float(self.data_item['Open'])
        self.high = float(self.data_item['High'])
        self.low = float(self.data_item['Low'])
        self.volume = float(self.data_item['Volume'])
        self.margin = float(self.data_item['%'])

        self.foriegn_buy = float(self.data_item['NN Mua'])
        self.foriegn_sell = float(self.data_item['NN Ban'])

    @property
    def price(self)->float:
        if self.close > 0:
            return self.close
        else:
            return self.open
    
    def isBreakFlat(self)->bool:
        length = 10
        max = np.max(self.df_all_data[1:length]['Close'])
        min = np.min(self.df_all_data[1:length]['Close'])
        high = ((max-min)/min)*100

        if high <= 7:
            if self.close > max:
                return True
        else:
            return False

    def isBreak52Week(self)->bool:
        length = 5*4*12
        max = np.max(self.df_all_data[1:length]['Close'])
        min = np.min(self.df_all_data[1:length]['Close'])
        print(f'{self.symbol} - max: {max} : min {min} : HT {self.close}')
        if self.close > max:
            return True
        else:
            return False

    def isInRangeMA(self, window:int)->bool:
        range = self.getRangeMA(window=window)
        price = self.price
        return range.isIn(price)

    def isInRangeMAs(self, windows:list[int])->bool:        
        results = []
        for w in windows:
            if self.isInRangeMA(window=w):
                if self.getMA(window=10) >= self.getMA(window=20):
                    results.append(w)
        if len(results) >= 2: #Tối thiểu nằm trong 02 MA khác nhau
            return True
        else:
            return False        

    def getRangeMA(self, window:int):
        ma_price = self.getMA(window=window)
        r = RangeMA(ma_price)
        return r

    def getMA(self, window:int)->float:
        df = self.df_all_data.sort_values(by=['Date'])
        short_rolling = df['Close'].rolling(window=window).mean()        
        value = short_rolling[0]
        return value

    def isThroughMA(self, window:int)->bool:
        low = self.low
        ma_price = self.getMA(window=window)
        if low < ma_price and self.close > ma_price:
            return True
        else:
            return False
    def isThroughMAs(self, windows:list[int])->bool:        
        results = []
        for w in windows:
            if self.isThroughMA(window=w):                
                    results.append(w)
        if len(results) >= 2: #Tối thiểu nằm trong 02 MA khác nhau
            return True
        else:
            return False
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
    
    def isUpVolume(self, rate:float, margin_price:float)->bool:
        '''
        current_vol >= rate*last_vol
        '''
        last_vol = self.df_all_data['Volume'].values[self.index+1]
        current_vol = self.df_all_data['Volume'].values[self.index]
        if self.symbol == "CEO":
            print(f'{self.symbol} - {self.date}')
            print(f'{current_vol} - {rate*last_vol}')
            print(f'{self.close} - {self.open}')
            sleep(5)
        if current_vol >= rate*last_vol:
            if self.close > self.open:
                return True
        else:
            return False

    def isMinVolume(self, window:int)->bool:
        '''
        current_vol >= rate*last_vol
        '''
        last_min_vol = np.min(self.df_all_data['Volume'].values[self.index+1:self.index+window])
        current_vol = self.df_all_data['Volume'].values[self.index]
        
        last_min_price = np.min(self.df_all_data['Close'].values[self.index+1:self.index+window])
        last_max_price = np.max(self.df_all_data['Close'].values[self.index+1:self.index+window])
        current_price = self.df_all_data['Close'].values[self.index]
        high_price = ((last_max_price-last_min_price)/last_min_price)*100

        rate = 1
        if current_vol <= rate*last_min_vol:
            if current_price <= last_max_price and current_price >= last_min_price:
                if high_price <= 5:
                    return True
        else:
            return False

    def isElephant(self, window:int)->bool:
        volume = self.volume
        max_volume = np.max(self.df_all_data['Volume'][self.index:self.index+window])
        pre_volumes = self.df_all_data['Volume'][self.index+1:self.index+window]
        rate = 3
        if np.min(pre_volumes)>=5:
            if self.close > self.open:
                if (volume >= rate*np.min(pre_volumes)) or (max_volume >= rate*np.min(pre_volumes)):
                    if self.close > self.open:
                        return True
        else:
            return False

    def isCover(self)->bool:
        before_data_item = self.df_all_data.iloc[self.index+1]
        if self.high > before_data_item['High']:
            if self.low < before_data_item['Low']:
                if self.close > before_data_item['High']:
                    return True
        else:
            return False

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
            if self.close > self.open:
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