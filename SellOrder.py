from DateHelper import NOW, percent
import pandas as pd
import json
from dataclasses import dataclass
from datetime import datetime
from OrderDb import OrderDb
from RichNumber import RichNumber
from db import get_now_price
from MongoDb import *

class Order:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()


class SellOrder:
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
        
    def to_string(self):        
        return f'{self.symbol} | Bán: {self.volume:,.0f} Giá: {self.price:,.0f} Thành tiền {self.income:,.0f}' +\
            f' Phí (bán): {self.fee:,.0f} Thuế (bán): {self.fee:,.0f} Tổng thu: {self.total_income:,.0f}'

    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

    def process(self):
        select_oder = self.get_buy_orders().iloc[0]
        sell_vol = self.volume
        buy_vol = select_oder['volume']
        
        total_vol = sell_vol - buy_vol
        if(total_vol == 0):
            print('Bán hết, vừa đủ')
        elif(total_vol > 0):
            print(f'Số lượng còn lại là: {total_vol}')
            #Bán chưa hết, vẫn còn, cần lấy thêm lệnh tiếp theo
        else:
            print(f'Vẫn còn dư mua, cập nhật lại số lượng')
            #Vẫn còn, cập nhật lại lệnh select_order hiện tại

        print('Đang xử lý lệnh bán')

    def get_buy_orders(self):
        _db = OrderDb()
        orders = _db.getStockOrders(symbol=self.symbol)
        orders = orders.sort_values(by=['price'])
        print(orders)
        return orders


s = SellOrder(symbol='BID',volume=100, price=10.55)
print(s.get_buy_orders())
s.process()

s = SellOrder(symbol='BID',volume=50, price=10.55)
print(s.get_buy_orders())
s.process()

s = SellOrder(symbol='BID',volume=150, price=10.55)
print(s.get_buy_orders())
s.process()