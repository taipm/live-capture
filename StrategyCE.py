from SellOrder import SellOrder
from BuyOrder import BuyOrder
import db
from DateData import DateData
from BlogManager import Blog

class StrategyCE:
    def __init__(self,symbol) -> None:
        self.name = 'BUY WITH FL and SELL with has profit'
        self.symbol = symbol.upper()
        self.df = db.GetStockData(symbol=self.symbol)
        self.length = len(self.df)
        self.startDate = self.df['Date'][self.length-1]
        self.endDate = self.df['Date'][0]

        self.dateData:DateData


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

        self.blog = Blog()
        self.start()

    def start(self):
        self.index = self.length - 1
        self.dateData = DateData(symbol=self.symbol,index=self.index,df_all_data=self.df)
    
    def next(self):
        self.index = self.index + 1
        self.dateData = DateData(symbol=self.symbol,index=self.index,df_all_data=self.df)

    def stop(self):
        pass

    def getBuySignals(self):
        pass

    def getSellSignals(self):
        pass

    def scan(self):
        for i in range(self.length):
            index = self.length - i - 1
            d = DateData(symbol=self.symbol,index=index,df_all_data=self.df)
            if d.isCE:
                method = 'CE'
                self.buy_signals.append([i,index,d.close,d.date,method,f''])
                b_order = BuyOrder(symbol=self.symbol,volume=self.volume_to_buy,price=d.close,date=d.date)
                b_order.addNote('CE')
                self.buy_orders.append(b_order)

    def excute(self):
        for i in range(self.buy_signals):
            buy = self.buy_signals[i]
            self.buy(volume=100,price=buy[1])

    def buy(self, volume, price, date):
        pass

    def sell(self):
        pass
    
    def currentInfo(self):
        output = f'\n{self.name} | {self.symbol}'
        output += f'\nĐang ở: {self.index}/{self.length}'
        output += self.dateData.__str__()


        return output

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

        #self.avg_price = self.amount/self.volume
    def getDate(self, index):
        return self.df['Date'][index]

    def Summary(self):
        self.update()
        output = f'Phương pháp: {self.name}'
        output += f'\nDỮ LIỆU'
        output += f'\nSố phiên {self.length} : Bắt đầu {self.startDate} đến {self.endDate}'
        output += f'\nSố lệnh mua {len(self.buy_orders)} | Số lệnh bán {len(self.sell_orders)}'
        output += f'\nTổng KL : {self.volume} : Giá TB {self.avg_price} : Thành tiền {self.cost}'
        
        for i in range (len(self.buy_signals)):
            output += f'\n Tín hiệu M thứ {i} - ngày {self.getDate(i)}: {self.buy_signals[i]}'
        
        # for i in range (len(self.sell_signals)):
        #     output += f'\n Tín hiệu B thứ {i}: {self.sell_signals[i]}'

        for o in self.buy_orders:
            output += f'\n Lệnh M : {o.__str__()}'
        
        # for i in range (len(self.sell_orders)):
        #     output += f'\n Lệnh B {i}: {self.sell_orders[i]}'
        output += f'{"-"}*30'
        url = self.blog.post(title=f'{self.name} - {self.Summary}', content=output,tags=['Strategy',f'{self.name}'])
        print(url)
        return output
        



s = StrategyCE(symbol='VND')
#print(s.Summary())

s.start()

info = s.currentInfo()
print(info)

s.scan()
print(s.Summary())