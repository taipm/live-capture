from datetime import datetime
from SellOrder import SellOrder
from BuyOrder import BuyOrder
import db
from DateData import DateData

class ElephantStrategy:
    def __init__(self,symbol) -> None:
        self.symbol = symbol.upper()
        self.df = db.GetStockData(symbol=self.symbol)
        self.length = len(self.df)
        self.window = 10
        self.buy_signals = []
        self.sell_signals = []
        self.buy_orders = []
        self.sell_orders = []

        self.volume = 0
        self.volume_to_buy = 100
        self.avg_price = 0
        self.cost = 0
        self.profit = 0

    def getBuySignals(self):
        pass

    def getSellSignals(self):
        pass
    
    def scan(self):
        for i in range(self.length):
            index = self.length - i
            d = DateData(symbol=self.symbol,index=index,df_all_data=self.df)
            if d.isElephant(window=self.window):
                self.buy_signals.append([i,index,d.close,d.date,'Elephants',f''])
                b_order = BuyOrder(symbol=self.symbol,volume=self.volume_to_buy,price=d.close,date=d.date)
                b_order.addNote('Elephant')
                self.buy_orders.append(b_order)


            # if d.isElephant(window=self.window):
            #     self.buy_signals.append([i,index,d.close,d.date,'Elephants',f''])
                #self.buy(volume=100,price=d.close,date=d.date)
    def excute(self):
        for i in range(self.buy_signals):
            buy = self.buy_signals[i]
            self.buy(volume=100,price=buy[1])

    def buy(self, volume, price, date):
        pass

    def sell(self):
        pass
    
    def update(self):
        self.volume = 0
        self.amount = 0
        self.avg_price = 0

        for i in range(len(self.buy_orders)):
            self.volume += self.buy_orders[i].volume
            self.cost += self.buy_orders[i].total_cost

        # for i in range(len(self.sell_orders)):
        #     self.volume -= self.sell_orders[i].volume
        #     self.amount -= self.sell_orders[i].total_income

        self.avg_price = self.amount/self.volume
        
    def Summary(self):
        self.update()
        output = f'Số lệnh mua {len(self.buy_orders)} | Số lệnh bán {len(self.sell_orders)}'
        output += f'\nTổng KL : {self.volume} : Giá TB {self.avg_price} : Thành tiền {self.cost}'
        
        for i in range (len(self.buy_signals)):
            output += f'\n Tín hiệu M: {self.buy_signals[i]}'
        
        for i in range (len(self.sell_signals)):
            output += f'\n Tín hiệu B: {self.sell_signals[i]}'

        for i in range (len(self.buy_orders)):
            output += f'\n Lệnh M: {self.buy_orders[i]}'
        
        for i in range (len(self.sell_orders)):
            output += f'\n Lệnh B: {self.sell_orders[i]}'

        return output


# s = ElephantStrategy(symbol='VPB')
# s.scan()
# print(s.Summary())

import pandas as pd
class Book:
    def __init__(self) -> None:
        self.buyOrders = []
        self.sellOrders = []
    def addBuy(order:BuyOrder):
        pass
    def addSell(order:SellOrder):
        pass

    def __str__(self) -> str:
        pass

class TradeEngine:
    def __init__(self, symbol, date:datetime, index:int) -> None:
        self.symbol = symbol.upper()
        self.date = date
        self.index = index
        self.df = db.GetStockData(symbol=self.symbol)
        self.length = len(self.df)
        self.startDate = self.df[self.length-1]['Date']
        self.endDate = self.df[self.length-1][0]        
        self.dateData = DateData(symbol=self.symbol, index=index,df_all_data=self.df)

        self.note = ''
        self.buyVol = 100
        self.book:Book

    def start(self):
        pass

    def reset(self):
        pass
    
    def run(self):

        pass

    def BuyFL(self):
        if self.dateData.isFL:
            order = BuyOrder(symbol=self.symbol,volume=self.buyVol,date=self.date)
            self.book.addBuy(order)
            

    def BuyCE(self):
        if self.dateData.isCE:
            order = BuyOrder(symbol=self.symbol,volume=self.buyVol,date=self.date)
            self.book.addBuy(order)

    def summary(self):
        output = f''
        if len(self.book.buyOrders) > 0:
            pass

        if len(self.book.sellOrders) > 0:
            pass

        return output

symbol = 'VND'
t = TradeEngine(symbol=symbol)
t.start()
s = t.summary()
print(s)

