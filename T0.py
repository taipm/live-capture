#from db import *
import math
from DateHelper import *
from StockTransaction import *
from db import get_now_price
class T0:
    def __init__(self,symbol, total_volume,origin_price) -> None:
        self.symbol = symbol.upper()
        self.total_volume = total_volume
        self.origin_price = origin_price
        self.market_price = get_now_price(self.symbol)
        t = Transaction(symbol=self.symbol,volume=self.total_volume,buy_price=self.origin_price,sell_price=self.market_price)
        self.total_cost = t.b_order.total_cost
        self.total_rate_profit = t.rate_profit
        self.total_profit = t.profit

        self.transaction_volume = self.volume_to_transaction()
        self.price = self.market_price
        self.pct_price = 3

        self.buy_price = inc_percent(self.price,-self.pct_price) #giảm 3% so với giá hiện tại, MUA
        self.sell_price = inc_percent(self.price,self.pct_price) #tăng 3% so với hiện tại, BÁN

        self.profit = 0
        self.rate_profit = 0
        self.cost = self.transaction_volume*self.price
        self.total_income = 0
        self.count_transaction = 0

    def volume_to_transaction(self):
        return self.total_volume/2

    def transaction(self):
        t = Transaction(symbol=self.symbol,volume=self.transaction_volume,sell_price=self.sell_price,buy_price=self.buy_price)
        self.profit += t.profit
        self.total_income += t.s_order.total_income
        self.count_transaction += 1

    def excute(self, n_transaction):
        for i in range(0,n_transaction):
            self.transaction()

    @property
    def summary(self):
        output = f'{self.symbol} - Total cost: {self.total_cost:,.0f} - B/HT: {self.origin_price:,.0f} | {self.market_price:,.0f} | LN: {self.total_profit:,.0f} ({self.total_rate_profit:,.2f})(%)'
        output += f'\nCount: {self.count_transaction}: {self.transaction_volume:,.0f} | Profit: {self.profit:,.2f} | TL: {(self.profit/self.cost)*100:,.2f} (%)| Money: {self.total_income:,.2f}'
        return output

t = T0(symbol='VGI',total_volume=2000,origin_price=24120)
print(t.summary)
while t.profit + t.total_profit <= 0:
    t.excute(1)
print(t.summary)

    
