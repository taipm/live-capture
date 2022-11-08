from DateHelper import NOW, percent
import pandas as pd
import xlsxwriter
import json
from bson import json_util
#import dataclasses
from dataclasses import dataclass
from datetime import datetime
class Order:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.time = NOW

class DatetimeEncoder(json.JSONEncoder):
    def default(self, ob):
        if isinstance(ob, datetime):
            return str(ob)
        return json.JSONEncoder.default(self, ob)
@dataclass
class BuyOrder:
    BSC_BUY_FEE = 0.1/100
    db_file = './data/TradingBook.xlsx'
    def __init__(self, symbol, volume, price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price
        self.time = str(NOW)
        self.type = 'BUY'

    @property
    def cost(self):
        return self.volume*self.price

    @property
    def fee(self):        
        return self.cost*self.BSC_BUY_FEE

    @property
    def total_cost(self):        
        return self.cost + self.fee

    def to_string(self):
        return f'{self.symbol} | Mua: {self.volume:,.0f} Giá: {self.price:,.0f} Phí (mua): {self.fee:,.0f} Tổng chi phí: {self.total_cost:,.0f}'

    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

class SellOrder:
    BSC_SELL_FEE = 0.1/100
    BSC_SELL_TAX = 0.01/100
    db_file = './data/TradingBook.xlsx'

    def __init__(self, symbol,volume, price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price
        self.time = str(NOW)
        self.type = 'SELL'
        
        
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

    def get_length(self):
        return len(pd.read_excel(self.db_file,sheet_name='SELL', engine='openpyxl'))

    def done(self):
        # book_data = pd.read_excel(self.db_file)
        # print(book_data)
        
        self.workbook = xlsxwriter.Workbook(self.db_file)
        self.worksheet = self.workbook.get_worksheet_by_name('SELL')
        len = self.get_length()+1
        self.worksheet.write_row(row=len,col=0, data=[self.symbol,self.volume,self.price, self.fee,self.income,self.total_income,self.time,self.type])
        self.workbook.close()
        
    def print_db_data(self):
        data = pd.read_excel(self.db_file,sheet_name='SELL', engine='openpyxl')
        print(data)

    def to_string(self):        
        return f'{self.symbol} | Bán: {self.volume:,.0f} Giá: {self.price:,.0f} Thành tiền {self.income:,.0f}' +\
            f'Phí (bán): {self.fee:,.0f} Thuế (bán): {self.fee:,.0f} Tổng thu: {self.total_income:,.0f}'

    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

# s = BuyOrder(symbol='VND',volume=1000,price=10)
# print(s.to_json())
# s.done()
# s.print_db_data()