from datetime import datetime
from BuyOrder import BuyOrder
from Caculator import *
from DateData import DateData
from SellOrder import *
from db import get_now_price
import db
from BlogManager import Blog, BlogPost

class TradingBook:
    def __init__(self, symbol:str, strategyName:str) -> None:
        self.symbol = symbol.upper()
        self.strategyName = strategyName

        self.df = db.GetStockData(symbol=symbol)
        self.df['Close']=self.df['Close']*1000

        self.buy_orders = []
        self.sell_orders = []
        self.df_orders:pd.DataFrame
        
        self.total_volume = 0
        self.avg_price = 0
        self.total_cost = 0

        self.total_profit = 0

        self.rate_of_profit = 0
        self.total_buy_fee = 0
        self.total_sell_fee = 0
        self.total_sell_tax = 0

        self.currentAmount = 0
        self.available_amount = 0
        self.startAmount = 0
        self.endAmount = 0

    def initial(self):
        self.total_volume = 0
        self.avg_price = 0
        self.total_cost = 0
        self.total_profit = 0
        #self.rate_of_profit = 0
        self.startAmount = 1000000000 #One billion
        self.available_amount = self.startAmount


    def getCandleStick(self, date): #-> Nên chuyển: CurrenData
        index = db.get_index_by_date(symbol=self.symbol, date=date)
        dateDate = DateData(symbol=self.symbol,index=index,df_all_data=self.df)
        self.currentIndex = index
        return dateDate
        
    def update(self):
        #print(f'Cost: {self.total_cost} - profit: {self.total_profit}')
        print(f'Mua: {len(self.buy_orders)} - Bán: {len(self.sell_orders)}')

        if self.total_volume > 0:
            self.avg_price = self.total_cost/self.total_volume
 
        self.total_profit = self.currentAmount - self.startAmount

        
        # if self.total_cost > 0:
        #     self.rate_of_profit = self.total_profit/self.total_cost

        
        self.df_b_orders = pd.DataFrame([t.__dict__ for t in self.buy_orders])
        self.df_s_orders = pd.DataFrame([t.__dict__ for t in self.sell_orders])

        self.df_orders = pd.DataFrame.empty
        self.df_orders  = self.df_b_orders.append(self.df_s_orders)
        #self.df_orders['avg-price'] = self.total_cost/self.df_orders['volume']
        self.df_orders = self.df_orders.sort_values(by=['date'])

    def addBuy(self, order:BuyOrder):
        self.buy_orders.append(order)
        self.total_volume += order.volume
        self.total_cost += order.total_cost
        self.update()
        print(f'B: Total cost {self.total_cost:,.2f} - Total volume : {self.total_volume:,.0f} - price: {order.price:,.2f}')
        # if self.rate_of_profit != None:
        #     print(f'Total volume {self.total_volume} - avg price: {self.avg_price:,.2f} | Profit: {self.rate_of_profit:,.2f}')
        # else:
        #     print(f'Total volume {self.total_volume} - avg price: {self.avg_price:,.2f} | Profit: {self.rate_of_profit}')

    def addSell(self, order:SellOrder):
        self.sell_orders.append(order)
        self.total_volume = self.total_volume - order.volume

        #self.total_cost = self.total_cost - order.total_income

        self.available_amount += order.total_income
        self.update()
        print(f'S: volume {self.total_volume} - Total volume : {self.total_volume} - avg price: {self.avg_price:,.2f}')
        

    def report(self):
        output = f'\n{self.symbol}'
        self.update()
        output += f'\nThuật toán: {self.strategyName}'
        output += f'\nTổng chi phí: {self.total_cost:,.0f} | Tổng KL: {self.total_volume:,.0f} - Giá TB: {self.avg_price:,.2f}'
        output += f'\nSức mua còn lại: {self.available_amount:,.0f} | Tổng lợi nhuận: {self.total_profit:,.2f} - Tỷ lệ: {self.rate_of_profit:,.2f}'
        output += f'\n{"-"*30}'
        if len(self.buy_orders) > 0:
            for i in range(len(self.buy_orders)):
                order = self.buy_orders[i]
                output += f'\n{order.date}[{i}] | Mua: {order.volume} - Giá: {order.price}'
                output += f'\nTín hiệu mua: {self.getCandleStick(date=order.date)}'
        
        if len(self.sell_orders) > 0:
            for i in range(len(self.sell_orders)):
                order = self.sell_orders[i]
                output += f'\n{order.date}[{i}] | Bán: {order.volume} - Giá bán: {order.price} - Thành tiền: {order.total_income:,.2f}'
                output += f'\nTín hiệu bán: {self.getCandleStick(date=order.date)}'

        output += self.df_orders.to_markdown()

        return output

class FLer(TradingBook):
    def __init__(self, symbol: str, strategyName: str, window:int,vol_to_buy:int) -> None:
        super().__init__(symbol, strategyName)
        self.df = self.df[0:window]
        self.length = len(self.df)
        self.currentIndex = self.length - 1
        self.currentDate:datetime
        self.startDate = self.df['Date'][self.currentIndex]
        self.endDate = self.df['Date'][0]
        
        self.vol_to_buy = vol_to_buy
        #self.total_cost = 0
        self.price = 0
        self.profit = 0
        self.textContent = ''
    
    def updateState(self):
        self.price = self.df.iloc[self.currentIndex]['Close']
        self.currentDate = self.df[self.df.index == self.currentIndex]['Date'].values[0]
        self.dateData = DateData(symbol=self.symbol,index=self.currentIndex,df_all_data=self.df)
        self.rate_of_profit = profit(self.avg_price, self.price)

    # @property
    # def rate_of_profit(self):
    #     if self.rate_of_profit == None:
    #         return "NA"
    #     return self.rate_of_profit
        
    # @rate_of_profit.setter
    # def rate_of_profit(self):
    #     return profit(self.avg_price, self.price)

    def canBuy(self):
        self.updateState()
        d = DateData(symbol=self.symbol,index=self.currentIndex,df_all_data=self.df)
        if d.isFL:
            return True
        return False
    
    def canSell(self):
        self.updateState()
        if self.total_volume <= 0:
            return False
      
        if self.rate_of_profit != None and float(self.rate_of_profit) >= 10:
            return True
        # d = DateData(symbol=self.symbol,index=self.currentIndex,df_all_data=self.df)
        # if d.isLowest:
        #     return True
        return False

    def getBuyPrice(self):
        self.updateState()
        price = self.df.iloc[self.currentIndex]['Close']
        return price

    def isTakeProfit(self):
        #self.updateState()
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

    def takeProfit(self):
        if self.canSell():
            info = f'KL: {self.total_volume} - Giá TB: {self.avg_price:,.2f} -> Giá HT: {self.price:,.2f} | {self.currentDate}'
            if self.rate_of_profit != None:
                info += f'\n{self.currentIndex} : Lợi nhuận: {self.rate_of_profit:,.2f} (%) - Có thể chốt lời'
            else:
                print(f'Rate of profite: None')
            print(info)
            self.textContent += f'\n{info}'
            d = self.step(index=self.currentIndex)
            self.sell(vol=self.total_volume,price=d.price,date=d.date)
            #self.updateState()
            #self.update()

    def step(self, index): #-> Nên chuyển: CurrenData
        dateDate = DateData(symbol=self.symbol,index=index,df_all_data=self.df)
        self.currentIndex = index
        return dateDate

    def buy(self, vol, price, date):
        b_order = BuyOrder(symbol=self.symbol,volume=vol,price=price,date=date)
        self.addBuy(order=b_order)

    def sell(self, vol, price, date):
        s_order = SellOrder(symbol=self.symbol,volume =vol, price = price, date=date)
        self.addSell(order=s_order)

    def calcBuyVolume(self):
        buy_volume = 0
        if self.total_volume == 0:
            buy_volume = self.vol_to_buy
        else:
            buy_volume = len(self.buy_orders)*self.vol_to_buy
        return buy_volume
            
    

    def excute(self):
        for i in range(self.length):
            index = self.length - 1 - i
            d = self.step(index=index)
            # if d.isFL:
            #     self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
            #     self.updateState()
            # if d.isHighest:
            #     self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
            #     self.updateState()
            if self.canBuy():
                #self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
                self.buy(vol=self.calcBuyVolume(),price=self.getBuyPrice(),date=d.date)
                self.updateState()
            
            # if self.canSell():
            #     #self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
            #     self.sell(vol=self.calcBuyVolume(),price=d.close,date=d.date)
            #     self.updateState()
            # if self.rate_of_profit < -10:
            #     self.buy(vol=self.calcBuyVolume(),price=d.price,date=d.date)
            #     self.updateState()

            self.takeProfit()
        
    def summary(self):
        self.updateState()
        output = f'symbol: {self.symbol}'
        output += f'\nLength: {self.length} | Start : {self.startDate} | End : {self.endDate}'
        output += self.report()

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
symbols = ['VCI']
window = 50
for symbol in symbols:
    c = FLer(symbol=symbol, vol_to_buy=100, window=window, strategyName='FL')
    c.excute()
    s = c.summary()
    print(s)
    #c.saveOnBlog()
