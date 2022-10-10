from helpers import percent
from stockApi import *
from Caculator import *
class TradingBook:
    def __init__(self,symbol) -> None:
        self.symbol = symbol.upper()
        self.sum_vol = 0
        self.sum_money = 0
        self.cost_price = 0
        self.market_price = 0

    def Buy(self, vol, price):
        self.sum_vol += vol
        self.sum_money += vol*price*1000
    
    def updateBook(self):
        self.cost_price = self.sum_money/self.sum_vol
        self.market_price = GetMarketPrice(self.symbol)

    def report(self):
        self.updateBook()
        output_text = f'{self.symbol} - vol: {self.sum_vol} - cost: {self.cost_price} ({percent(self.market_price, self.cost_price)})'
        return output_text

    