import json
from BuyOrder import BuyOrder
from MongoDb import MongoDb
from OrderDb import OrderDb, TransactionDb
from SellOrder import SellOrder
from DateHelper import percent

class Transaction:
    def __init__(self, symbol, volume, buy_price, sell_price) -> None:
        self.symbol = symbol.upper()
        self.volume = volume
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.b_order = BuyOrder(symbol=self.symbol,volume=self.volume, price=self.buy_price)
        self.s_order = SellOrder(symbol=self.symbol,volume=self.volume, price=self.sell_price)
        self.profit = self.get_profit()
        self.rate_profit = self.get_rate_profit()

     
    def get_profit(self):
        profit = self.s_order.total_income - self.b_order.total_cost
        return profit

    def get_rate_profit(self):
        rate_profit = percent(self.b_order.total_cost, self.s_order.total_income)
        return rate_profit
    
    def excute(self):
        '''
        Thực thi transaction
        '''
        select_oder = self.get_buy_orders().iloc[0]
        sell_vol = self.volume
        buy_vol = select_oder['volume']
        
        total_vol = sell_vol - buy_vol
        if(total_vol == 0):
            print('Bán hết, vừa đủ')
        elif(total_vol > 0):
            print(f'Số lượng còn lại là: {total_vol}')
            #Bán chưa hết, vẫn còn, cần lấy thêm lệnh tiếp theo
        else:
            print(f'Vẫn còn dư mua, cập nhật lại số lượng')
            #Vẫn còn, cập nhật lại lệnh select_order hiện tại

        print('Đang xử lý lệnh bán')
        db = TransactionDb()
        #t = Transaction(symbol=self.symbol,volume=self.volume, buy_price=self.buy_price,sell_price=self.sell_price)
        #print(t.to_json)
        db.add_item(self.to_json())
    
    def get_buy_orders(self):
        _db = OrderDb()
        orders = _db.getStockOrders(symbol=self.symbol)
        orders = orders.sort_values(by=['price'])
        print(orders)
        return orders

    def to_string(self):
        return f'{self.symbol} | {self.volume:,.0f} Mua {self.buy_price} - Bán {self.sell_price} -> Lợi nhuận: {self.profit:,.0f} ({self.rate_profit:,.2f}(%))'
    
    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

def test():
    order = BuyOrder(symbol="VND",volume=100,price=17500)
    print(order.to_string())

    s_order = SellOrder(symbol="KSB",volume=500,price=17350)
    print(s_order.to_string())

    t = Transaction(symbol='BSR',volume=2000,buy_price=17700, sell_price=17800)
    t.excute()
    print(t.to_string())

test()