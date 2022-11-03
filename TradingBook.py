from DateHelper import percent
from Caculator import *
import pandas as pd
from StockOrder import *
class TradingBook:
    def __init__(self,symbol) -> None:
        self.symbol = symbol.upper()
        self.sum_vol = 0
        self.sum_money = 0
        self.cost_price = 0
        self.market_price = 0
        self.db_file = self.symbol + '-TradingBook.xlsx'
        self.df = pd.DataFrame()

    def load_book(self):
        self.df = pd.read_excel(self.db_file)
        print(self.df)

    def update_order(self, vol, price):
        pass

    def Buy(self, vol, price):
        self.sum_vol += vol
        self.sum_money += vol*price*1000

        self.df.to_excel(self.db_file)
        self.updateBook()
    
    def updateBook(self):

        self.cost_price = self.sum_money/self.sum_vol
        self.market_price = -1 #GetMarketPrice(self.symbol)

    def report(self):
        self.updateBook()
        output_text = f'{self.symbol} - vol: {self.sum_vol} - cost: {self.cost_price} ({percent(self.market_price, self.cost_price)})'
        return output_text


# t = TradingBook(symbol='VND')
# t.Buy(vol=100,price=10)
