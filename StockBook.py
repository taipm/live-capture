from BuyOrder import BuyOrder
from OrderDb import *
from SellOrder import SellOrder

class StockBook:
    db_file = './data/TradingBook.xlsx'
    def __init__(self,symbol) -> None:        
        self.symbol = symbol.upper()
        self.db = OrderDb()
        self.df_data =  pd.DataFrame(list(self.db.getStockOrders(symbol=self.symbol)))
        
    @property
    def summary(self):
        output = f'Length: {len(self.df_data)}'
        return output
        
    def sum(self):
        print(f'Tổng lệnh: {len(self.df_data)}')
        print(self.df)
    
    @property
    def Orders(self):
        orders = []
        for i in range(0,len(self.df_data)-1):
            item = self.df_data.iloc[i]
            query = {'time':item['time']}
            order = self.db.getOrder(query=query)
            if(order['type']=='BUY'):
                o = BuyOrder(symbol=order['symbol'],volume=order['volume'],price=order['price'])
                o.time = order['time']
                orders.append(o)
            elif(order['type']=='SELL'):
                o = SellOrder(symbol=order['symbol'],volume=order['volume'],price=order['price'])
                o.time = order['time']
                orders.append(o)

        return orders

    @property
    def cost(self):
        sum_cost = 0
        for o in self.Orders:
            if o.type == 'BUY':
                sum_cost += o.total_cost
        return sum_cost

# o = StockBook(symbol='VND')
# orders = o.Orders
# #print(o.summary)
# for x in o.Orders:
#     print(x.to_string())
# print(f'Tổng chi phí: {o.cost:,.2f}')
# # d = MongoDb()
# # d.to_string()

# db = OrderDb()
# # db.print_data()

# # _order = BuyOrder(symbol='VND',volume=1000,price=117.8)
# # db.addOder(order=_order.to_json())
# # db.to_string()

# _order = SellOrder(symbol='VND',volume=-1000,price=17.8)
# db.addOder(order=_order.to_json())
# db.to_string()s