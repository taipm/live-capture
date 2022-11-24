from BuyOrder import BuyOrder
from Caculator import *
import pandas as pd
from DayData import DayData
from SellOrder import *
from Stock import Stock
from StockTransaction import Transaction
from db import get_now_price
class TradingBook:
    def __init__(self,symbol) -> None:
        self.stock = Stock(symbol)

        self.symbol = symbol.upper()
        self.total_volume = 0
        self.total_cost = 0
        self.avg_price = 0
        self.total_profit = 0
        self.db_file = f'{self.symbol}-TradingBook.xlsx'

    def buy(self, volume, price):
        t = BuyOrder(symbol=self.symbol,volume=volume,price=price)
        self.total_volume += t.volume
        self.total_cost += t.total_cost

        self.updateBook()

    def sell(self, volume, price):
        #Hiện tại đã bị trừ thuế, do đó cái này bị thuế 2 lần (có thể tạo đối tượng mới để xly)
        t = Transaction(symbol=self.symbol,volume=volume,buy_price=self.avg_price,sell_price=price) 
        self.total_profit += t.profit
        self.total_volume -= t.volume
        self.total_cost -= t.b_order.total_cost

        self.updateBook()

    def updateBook(self):
        self.avg_price = self.total_cost/self.total_volume
        print(self.to_string())
    
    def to_string(self):
        output = f'{self.symbol} | volume: {self.total_volume:,.0f} | cost: {self.total_cost:,.2f} | Giá TB {self.avg_price:,.2f}'
        return output

class FLer(TradingBook):
    def __init__(self, symbol) -> None:
        super().__init__(symbol)
        self.df_orders = self.buy_FL()
        self.df_data = self.stock.df_data
    
    def buy_FL(self)->pd.DataFrame:
        buy_volume = 100
        count = 0
        orders = []
        end = self.stock.len-1
        for i in range(0, self.stock.len-1):
        #for i in range(0, 10):
            index = end-i
            day = DayData(index=index,symbol=self.symbol,df_all_data=self.stock.df_data,count_days=10) #count_days chưa hợp lý
            #while count <= 20:
            if day.isFL:
                print(f'{index} - M {day.price} : T0 {day.high} - {day.t0_profit:,.2f} (%) | LN {day.T_days} : {day.max_profit:,.2f}')
                self.buy(volume= buy_volume, price= day.price)
                orders.append([buy_volume,day.price,day.index,day.date])
                count += 1
        return pd.DataFrame(list(orders),columns=['volume','price','index','date'])

    def process(self):
        print(self.df_orders)
        for i in range(0,len(self.df_orders)-1):
            item = self.df_orders.iloc[i]
            index = item['index']
            if index >= 10:
                max_price = np.max(self.df_data.iloc[index-10:index-3]['Close'])
                if(max_price > item['price']):
                    print(f'{i} -> {i-3}: Có lời {max_price}')
                else:
                    print(f'{i} -> {i-3}: LÕM')
            else:
                print('Chưa đủ 10 phiên, đang theo dõi')

    def summary(self):
        
        avg_price = self.total_cost/self.total_volume
        avg_price=avg_price*1000

        price = get_now_price(self.symbol)
        t = Transaction(symbol=self.symbol,volume=self.total_volume,buy_price=avg_price,sell_price=price)
        output = f'{self.symbol} | volume: {self.total_volume:,.0f} | cost: {self.total_cost:,.2f} | price {avg_price:,.2f} - {price:,.2f} '
        output += f'LN: {t.profit:,.2f} | {t.rate_profit:,.2f} (%)'
        return output

# f = FLer(symbol='HAX')
# f.buy_FL()
# print(f.summary())
# f.process()
