from datetime import datetime
from BuyOrder import BuyOrder
from Caculator import *
import pandas as pd
from DateData import DateData
from DayData import DayData
from SellOrder import *
from Stock import Stock
from StockTransaction import Transaction
from db import get_now_price
import db
from BlogManager import Blog, BlogPost

class TradingBookT0:
    def __init__(self, symbol, vol_to_buy:int, window:int) -> None:        
        self.symbol = symbol.upper()
        self.name = f'#DCA - MUA BÁN T0 {self.symbol}'
        self.df = db.GetStockData(symbol=symbol)[0:window]
        self.length = len(self.df)
        self.currentIndex = self.length - 1
        self.currentDate:datetime
        self.startDate = self.df['Date'][self.currentIndex]
        self.endDate = self.df['Date'][0]
        self.buy_orders = []
        self.sell_orders = []

        self.vol_to_buy = vol_to_buy
        self.total_volume = 0
        self.total_cost = 0
        self.avg_price = 0
        self.price = 0
        self.profit = 0
        self.total_profit = 0
        self.rate_of_profit = 0
        self.textContent = ''
    
    def updateState(self):
        self.price = self.df.iloc[self.currentIndex]['Close']
        self.currentDate = self.df[self.df.index == self.currentIndex]['Date'].values[0]
        if self.total_volume > 0:
            self.avg_price = self.total_cost/self.total_volume
            self.rate_of_profit = ((self.price - self.avg_price)/self.avg_price)*100
            #print(f'-> {self.price} - {self.currentIndex} {self.currentDate} - {self.profit:,.2f} - {self.rate_of_profit:,.2f}')

    def resetState(self):
        self.avg_price = 0
        self.profit = 0
        self.rate_of_profit = 0
        self.total_cost = 0
        self.total_volume = 0

    def takeProfit(self):
        if self.isTakeProfit():
            info = f'KL: {self.total_volume} - Giá TB: {self.avg_price:,.2f} -> Giá HT: {self.price:,.2f} | {self.currentDate}'
            info += f'\n{self.currentIndex} : Lợi nhuận: {self.rate_of_profit:,.2f} (%) - Có thể chốt lời'
            print(info)
            self.textContent += f'\n{info}'
            d = self.step(index=self.currentIndex)
            self.sell(vol=self.total_volume,price=d.price,date=d.date)
            self.resetState()
            self.updateState()
            
    def isTakeProfit(self):
        self.updateState()
        d = DateData(symbol=self.symbol,index=self.currentIndex,df_all_data=self.df)
        if d.isHighest:
            return False
        if d.isCE:
            return False
        if d.isGreen:
            return False

        if self.rate_of_profit >= 5:
            return True
        else:
            return False

    def step(self, index): #-> Nên chuyển: CurrenData
        dateDate = DateData(symbol=self.symbol,index=index,df_all_data=self.df)
        self.currentIndex = index
        return dateDate

    def buy(self, vol, price, date):
        b_order = BuyOrder(symbol=self.symbol,volume=vol,price=price,date=date)
        self.total_volume += b_order.volume
        self.total_cost += b_order.total_cost
        self.buy_orders.append(b_order)

    def calcBuyVolume(self):
        buy_volume = 0
        if self.total_volume == 0:
            buy_volume = self.vol_to_buy
        else:
            buy_volume = len(self.buy_orders)*self.vol_to_buy
        return buy_volume
            
    def sell(self, vol, price, date):
        s_order = SellOrder(symbol=self.symbol,volume =vol, price = price, date=date)
        self.sell_orders.append(s_order)
        self.total_volume = self.total_volume - s_order.volume
        self.total_profit += s_order.total_income
        
    def excute(self):
        for i in range(self.length):
            index = self.length - 1 - i
            d = self.step(index=index)
            if d.isFL:
                self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
                self.updateState()
            if d.isHighest:
                self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
                self.updateState()
            # if self.rate_of_profit < -10:
            #     self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
            #     self.updateState()

            self.takeProfit()
        
    def summary(self):
        self.updateState()
        output = f'symbol: {self.symbol}'
        output += f'\nLength: {self.length} | Start : {self.startDate} | End : {self.endDate}'

        if len(self.buy_orders) >0 :
            output += f'\nBuy Orders: '
            for i in range (len(self.buy_orders)):
                order = self.buy_orders[i]
                output += f'\n{i} - {order.date} - KL: {order.volume} - Giá mua: {order.price}'

        if len(self.sell_orders) >0 :
            output += f'\nSell Orders: '
            for i in range (len(self.sell_orders)):
                order = self.sell_orders[i]
                output += f'\n{i} - {order.date} - KL: {order.volume} - Giá bán: {order.price} - Money: {order.total_income*1000:,.2f}'

        output += f'\nTÓM TẮT: {self.symbol}\n'
        output += f'\nTổng số lệnh mua: {len(self.buy_orders)} - Tổng số lệnh bán: {len(self.sell_orders)}'
        output += f'\nKhối lượng: {self.total_volume:,.0f} - Tổng chi phí: {self.total_cost:,.2f} - Giá TB: {self.avg_price:,.2f}'
        output += f'\nTổng LN: {self.profit*1000:,.2f} - {self.rate_of_profit:,.2f} (%) - HT: {self.currentIndex} : {self.price}'
        output += f'\nTổng LN: {self.total_profit*1000:,.0f}'
        output += f'\n{"-"*30}\n'
        return output

    def saveOnBlog(self):
        title = self.name
        content = self.summary() + f'\n{self.textContent}'
        tags = ['#DCA', 'Chiến lược', 'TradingBook', 'Strategy']
        post = BlogPost(title=title,content=content,tags=tags)
        link = post.update_to_blog()
        print(link)

#symbols = ['FRT', 'BSI','VIB']
#symbols = ['FPT', 'MWG','SCR', 'NVL']
symbols = ['FRT']
for symbol in symbols:
    c = FL_er(symbol=symbol, vol_to_buy=100, window=5*52)
    c.excute()
    s = c.summary()
    print(s)
    c.saveOnBlog()    
