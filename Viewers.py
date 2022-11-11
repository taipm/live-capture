from MongoDb import OrderDb
from RichNumber import RichNumber
from StockOrder import BuyOrder
import pandas as pd
from DateHelper import *

class ViewOrders:
    def __init__(self) -> None:
        self.df_data = OrderDb().getOrders()
        self.df_buy_oders = self.get_df_buy_orders()
        self.count_of_oders = len(self.df_buy_oders)
        print(self.df_data)
    
    def get_df_buy_orders(self):
        orders = []
        for i in range(0, len(self.df_data)):
            item = self.df_data.iloc[i]
            if (item['type']=='BUY'):
                order = BuyOrder(symbol=item['symbol'],volume=item['volume'],price=item['price'])
                if(order.market_price > 0):
                    data_item = [order.symbol,order.volume, order.price, order.total_cost, order.market_price, order.current_profit, order.current_rate_profit]
                    orders.append(data_item)
        df = pd.DataFrame(list(orders), columns=['symbol','volume','price', 'total_cost', 'm_price','profit','%'])
        return df

    @property
    def total_buy_money(self):
        return np.sum(self.df_buy_oders['total_cost'])

    def notes(self, pct):
        output = ''
        if(pct >= 3):
            output += 'Nên chốt lời'
        if len(output) > 1:
            output = 'Note:\n' + output
        return output
    def to_tele_view(self):        
        df_view = self.df_buy_oders
        df_view = df_view[['symbol','volume','price', 'm_price','profit','%']]
        df_view['%'] = df_view['%'].map('{:,.2f}'.format)
        df_view['volume'] = (df_view['volume']).map('{:,.0f}'.format)
        df_view['price'] = (df_view['price']/1000).map('{:,.2f}'.format)
        df_view['m_price'] = (df_view['m_price']/1000).map('{:,.2f}'.format)
        df_view['profit'] = (df_view['profit']).map(lambda x:RichNumber(float(x)).toText())
        df_view['Note'] = df_view['%'].map(lambda x: self.notes(float(x)))
        return df_view
    
    def save_to_blog(self):
        pass

# v = ViewOrders()
# print(v.to_tele_view())
# print(f'{v.total_buy_money:,.2f}')