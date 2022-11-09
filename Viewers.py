from MongoDb import OrderDb
from StockOrder import BuyOrder
import pandas as pd
from DateHelper import *

class ViewOrders:
    def __init__(self) -> None:
        self.df_data = OrderDb().getOrders()
        self.df_view = self.to_view()
        print(self.df_data)
    
    def to_view(self):
        orders = []
        for i in range(0, len(self.df_data)):
            item = self.df_data.iloc[i]
            if (item['type']=='BUY'):
                order = BuyOrder(symbol=item['symbol'],volume=item['volume'],price=item['price'])
                if(order.market_price > 0):
                    data_item = [order.symbol,order.volume, order.price, order.total_cost, order.market_price, order.current_profit, order.current_rate_profit,order.time]
                    orders.append(data_item)

        pd.options.display.float_format = '{:,.0f}'.format
        df_view = pd.DataFrame(list(orders), columns=['symbol','volume','price', 'total_cost', 'm_price','profit','%','time'])
        df_view['%'] = df_view['%'].map('{:,.2f}'.format)
        df_view['price'] = (df_view['price']/1000).map('{:,.2f}'.format)
        df_view['m_price'] = (df_view['m_price']/1000).map('{:,.2f}'.format)
        df_view['profit'] = (df_view['profit']/million).map('{:,.2f}'.format)
        df_view['total_cost'] = (df_view['total_cost']/million).map('{:,.2f}'.format)
        df_view['time'] = df_view['time'].map(lambda x: x.split(' ')[0])

        return df_view
    
    def save_to_blog(self):
        pass

# v=ViewOrders()
# print(v.df_view)