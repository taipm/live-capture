from DateHelper import NOW
from Constant import *
import json
from dataclasses import dataclass
from MongoDb import *

class Order:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()


class SellOrder(ObjectDb):
    BSC_SELL_FEE = 0.1/100
    BSC_SELL_TAX = 0.01/100

    def __init__(self, symbol,volume, price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price
        self.time = str(NOW)
        self.type = 'SELL'
        #self.market_price = 0
                
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
        
    def __str__(self):        
        return f'{self.symbol} | Bán: {self.volume:,.0f} Giá: {self.price:,.0f} Thành tiền {self.income:,.0f}' +\
            f' Phí (bán): {self.fee:,.0f} Thuế (bán): {self.fee:,.0f} Tổng thu: {self.total_income:,.0f}'

    # def to_json(self):
    #     return json.dumps(self,default=lambda o: o.__dict__)