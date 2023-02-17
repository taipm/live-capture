from dataclasses import dataclass
#import json
from DateHelper import NOW
from MongoDb import ObjectDb
from OrderDb import OrderDb
from RichNumber import RichNumber
from db import get_now_price


@dataclass
class BuyOrder(ObjectDb):
    BSC_BUY_FEE = 0.1/100
    BSC_SELL_FEE = 0.1/100
    BSC_SELL_TAX = 0.1/100

    def __init__(self, symbol, volume, price, date) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.price = price
        self.time = str(NOW)
        self.type = 'BUY'
        self.date = date
        self.market_price = 0 #get_now_price(self.symbol)
        #self.market_price = get_now_price(self.symbol)
        self.note = ''

    def addNote(self, note):
        self.note += note

    def update(self):
        print(self.symbol)
        self.market_price = get_now_price(self.symbol)
        print(f'{self.symbol} : {self.market_price}')

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
        db = OrderDb()
        db.addItem(self)

    def __str__(self):
        output = f'{self.symbol} : {self.date}'
        output += f'\nMua: {self.volume:,.0f} Giá: {self.price:,.0f} Phí (mua): {self.fee:,.0f} Tổng chi phí: {self.total_cost:,.0f}' +\
                f'\nGiá HT {self.market_price:,.2f} | LN: {RichNumber(self.current_profit).toText()} | Tỷ lệ: {self.current_rate_profit:,.2f} (%)'

        return output
