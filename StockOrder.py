from DateHelper import NOW, percent
import pandas as pd
#import xlsxwriter
import json
#from bson import json_util
#import dataclasses
from dataclasses import dataclass
from datetime import datetime
from db import get_now_price
import MongoDb as MongoDb

class Order:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()

@dataclass
class BuyOrder:
    BSC_BUY_FEE = 0.1/100
    BSC_SELL_FEE = 0.1/100
    BSC_SELL_TAX = 0.01/100

    def __init__(self, symbol, volume, price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price
        self.time = str(NOW)
        self.type = 'BUY'
        self.market_price = get_now_price(self.symbol)

    @property
    def cost(self):
        return self.volume*self.price

    @property
    def fee(self):        
        return self.cost*self.BSC_BUY_FEE

    @property
    def total_cost(self):        
        return self.cost + self.fee
        
    @property
    def avg_price(self):
        return self.total_cost/self.volume

    @property
    def current_profit(self):
        sell_income = self.volume*self.market_price
        sell_fee = sell_income*self.BSC_SELL_FEE
        sell_tax = sell_income*self.BSC_SELL_TAX
        sell_total_income = sell_income - sell_fee - sell_tax
        return sell_total_income - self.total_cost
    
    @property
    def current_rate_profit(self):
        return (self.current_profit/self.total_cost)*100

    def save_to_db(self):
        db = MongoDb.OrderDb()
        order = self        
        db.addOder(order=order.to_json())

    def to_string(self):
        return f'{self.symbol} | Mua: {self.volume:,.0f} Giá: {self.price:,.0f} Phí (mua): {self.fee:,.0f} Tổng chi phí: {self.total_cost:,.0f}' +\
                f'\nGiá HT {self.market_price:,.2f} | LN: {self.current_profit:,.2f} Tỷ lệ: {self.current_rate_profit:,.2f} (%)'

    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

# b = BuyOrder(symbol='HAX',volume=700,price=16510)
# #print(b.avg_price)
# print(b.market_price)
# print(f'{b.current_profit:,.2f}')
# print(f'{b.current_rate_profit:,.2f} (%)')
# print(b.to_string())

class SellOrder:
    BSC_SELL_FEE = 0.1/100
    BSC_SELL_TAX = 0.01/100

    def __init__(self, symbol,volume, price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price
        self.time = str(NOW)
        self.type = 'SELL'
        self.market_price = get_now_price(self.symbol)
                
    @property
    def income(self):
        return self.volume*self.price

    @property
    def fee(self):        
        return self.income*self.BSC_SELL_FEE
    
    @property
    def tax(self):        
        return self.income*self.BSC_SELL_TAX
    
    @property
    def total_income(self):        
        return self.income - self.tax - self.fee
        
    def to_string(self):        
        return f'{self.symbol} | Bán: {self.volume:,.0f} Giá: {self.price:,.0f} Thành tiền {self.income:,.0f}' +\
            f'Phí (bán): {self.fee:,.0f} Thuế (bán): {self.fee:,.0f} Tổng thu: {self.total_income:,.0f}'

    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

