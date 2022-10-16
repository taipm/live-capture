
import datetime
from datetime import timedelta 
import db
from DateHelper import *
import pandas as pd

class DateStick:
    def __init__(self, symbol, date, close, high, low, open, volume) -> None:
        self.symbol = symbol.upper()
        self.date  = date
        self.close = close
        self.open = open
        self.high = high
        self.low = low
        self.volume = volume
    # def __init__(self, symbol, date) -> None:
    #     self.symbol = symbol.upper()
    #     self.date = date
    #     df_data = DayData(self.symbol).get_date_data_stick(date=date)
    #     self.close = df_data['Close']
    #     self.open = df_data['Open']
    #     self.high = df_data['High']
    #     self.low = df_data['Low']
    #     self.volume = df_data['Volume']
    def to_string(self):
        print(f'CP: {self.symbol} Close: {self.close} Open: {self.open} High: {self.high}')

    def is_up(self) -> bool:
        if (self.close == self.high):
            return True
    
    def is_down(self) -> bool:
        if(self.close == self.low):
            return True

    def forcast(self):
        if self.is_up():
            return 'UP'
        elif self.is_down():
            return 'DOWN'
        else:
            return None     

    def get_next_day_stick(self):
        next_date = self.date - timedelta(days = 1)
        
    #def check_forcast(self):

class DayData:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.df_data = db.GetStockData(self.symbol)

    def get_date_data_stick(self,date):
        data = self.df_data[self.df_data['Date'] == parse_text_to_date(date)]
        print(data)
        print(data['Open'])
        print(data['Close'])
        print(data['High'])
        print(data['Low'])

        date_stick = DateStick(symbol=self.symbol,
            date = date,
            open = data['Open'].values,
            close = data['Close'].values,
            high = data['High'].values,
            low = data['Low'].values,
            volume= data['Volume'].values
        )
        return date_stick

d = DayData(symbol='VND')
date_stick = d.get_date_data_stick(date='2022-10-14')
date_stick.to_string()

print(date_stick.symbol)
print(date_stick.open)
print(date_stick.forcast())

# stick = DateStick(symbol='VND')
# stick.forcast()
# print(date_stick.volume)


