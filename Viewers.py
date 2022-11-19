from BuyOrder import BuyOrder
from OrderDb import OrderDb
from RichNumber import RichNumber
import pandas as pd
from DateHelper import *
from db import *
class ViewOrders:
    def __init__(self) -> None:
        self.df_data = OrderDb().getOrders()
        self.df_buy_oders = pd.DataFrame()#self.get_df_buy_orders()
        self.count_of_oders = 0# len(self.df_buy_oders)
        #print(self.df_data)
    
    def get_df_buy_orders(self):
        orders = []
        for i in range(0, len(self.df_data)):
            item = self.df_data.iloc[i]
            if (item['type']=='BUY'):
                order = BuyOrder(symbol=item['symbol'],volume=item['volume'],price=item['price'])
                order.update()
                if(order.market_price > 0):
                    data_item = [order.symbol,order.volume, order.price, order.total_cost, order.market_price, order.current_profit, order.current_rate_profit]
                    orders.append(data_item)
        df = pd.DataFrame(list(orders), columns=['symbol','volume','price', 'total_cost', 'm_price','profit','%'])
        return df

    def get_df_buy_orders_by_stock(self, symbol):
        df = self.df_data[self.df_data['symbol'] == symbol.upper()]
        print(df)
        orders = []
        for i in range(0, len(df)):
            item = df.iloc[i]
            if (item['type']=='BUY'):
                order = BuyOrder(symbol=item['symbol'],volume=item['volume'],price=item['price'])
                order.update()
                if(order.market_price > 0):
                    data_item = [order.symbol,order.volume, order.price, order.total_cost, order.market_price, order.current_profit, order.current_rate_profit]
                    orders.append(data_item)
        df = pd.DataFrame(list(orders), columns=['symbol','volume','price', 'total_cost', 'm_price','profit','%'])
        return df

    @property
    def total_buy_money(self):
        print(f'money: {np.sum(self.df_buy_oders["total_cost"])}')
        return np.sum(self.df_buy_oders['total_cost'])
    @property
    def total_profit(self):
        return np.sum(self.df_buy_oders['profit'])
    @property
    def total_cost(self):
        return np.sum(self.df_buy_oders['total_cost'])

    def notes(self, pct):
        output = ''
        if(pct >= 3):
            output += 'Nên chốt lời'
        if len(output) > 1:
            output = 'Note:\n' + output
        return output

    def to_tele_view(self):        
        df_view = self.get_df_buy_orders()
        df_view = df_view[['symbol','volume','price', 'm_price','profit','%']]        
        df_view['volume'] = (df_view['volume']).map('{:,.0f}'.format)
        df_view['price'] = (df_view['price']/1000).map('{:,.2f}'.format)
        df_view['m_price'] = (df_view['m_price']/1000).map('{:,.2f}'.format)
        df_view['profit'] = (df_view['profit']).map(lambda x:RichNumber(float(x)).toText())
        df_view['%'] = df_view['%'].map('{:,.2f}'.format)
        df_view['Note'] = df_view['%'].map(lambda x: self.notes(float(x)))
        df_view = df_view.sort_values(by=['%'])
        output = df_view.to_markdown()
        output += f'\n Tổng vốn: {self.total_cost:,.0f} | Tổng lợi nhuận: {self.total_profit:,.0f} | {(self.total_profit/self.total_cost)*100:,.2f} (%))'
        return output

    def to_views(self, symbol):
        df_view = self.get_df_buy_orders_by_stock(symbol=symbol.upper())
        df_view = df_view[['symbol','volume','price', 'm_price','profit','%']]
        
        df_view['Note'] = df_view['%'].map(lambda x: self.notes(float(x)))

        rs = []
        for i in range(0,len(df_view)):
            item = df_view.iloc[i]
            symbol = item['symbol']
            volume = item['volume']
            price = item['price']
            m_price = item['m_price']
            _profit = item['profit']
            rate_profit = item['%']

            max_price = float(get_now_full_price(symbol=symbol)[1])
            min_price = float(get_now_full_price(symbol=symbol)[2])
            max_profit = profit(price,max_price)
            min_profit = profit(price,min_price)

            rs.append([symbol,volume,price,m_price,_profit, rate_profit, max_price,max_profit,min_price,min_profit])

        df = pd.DataFrame(list(rs),columns=['symbol','volume','price', 'm_price','profit','%','max_price','max_%','min_price','min_%'])
        df = df.sort_values(by=['%'])

        summary = f'\n{symbol} | {np.sum(df["volume"]):,.0f} : Tổng lợi nhuận: {np.sum(df["profit"]):,.2f}'
        
        df['max_price'] = (df['max_price']/1000).map('{:,.2f}'.format)
        df['min_price'] = (df['min_price']/1000).map('{:,.2f}'.format)
        df['volume'] = (df['volume']).map('{:,.0f}'.format)
        df['price'] = (df['price']/1000).map('{:,.2f}'.format)
        df['m_price'] = df['symbol'].map(lambda x: get_now_price(x))
        df['m_price'] = (df['m_price']/1000).map('{:,.2f}'.format)
        df['profit'] = (df['profit']).map(lambda x:RichNumber(float(x)).toText())
        df['%'] = df['%'].map('{:,.2f}'.format)
        df['max_%'] = df['max_%'].map('{:,.2f}'.format)
        df['min_%'] = df['min_%'].map('{:,.2f}'.format)
        
        output = df.to_markdown()
        output += summary
        return output

    def save_to_blog(self):
        pass

# print('Đang test Viewers')
# v = ViewOrders()
# print(v.to_views(symbol='VGI'))

# class TeleViewer:
#     def __init__(self) -> None:
#         self.orderDb = OrderDb()
#         self.df_data = self.orderDb.getOrders()
        

#     def get_buy_orders(self)->pd.DataFrame:
#         orders = []
#         for i in range(0, len(self.df_data)):
#             item = self.df_data.iloc[i]
#             if (item['type']=='BUY'):
#                 order = BuyOrder(symbol=item['symbol'],volume=item['volume'],price=item['price'])
#                 order.update()
#                 if(order.market_price > 0):
#                     data_item = [order.symbol,order.volume, order.price, order.total_cost, order.market_price, order.current_profit, order.current_rate_profit]
#                     orders.append(data_item)
#         df = pd.DataFrame(list(orders), columns=['symbol','volume','price', 'total_cost', 'm_price','profit','%'])
#         return df
    
#     def get_stocks_buy_orders(self, symbol)->pd.DataFrame:
#         orders = []
#         for i in range(0, len(self.df_data)):
#             item = self.df_data.iloc[i]
#             if (item['type']=='BUY' and item['symbol'] == symbol):
#                 order = BuyOrder(symbol=item['symbol'],volume=item['volume'],price=item['price'])
#                 order.update()
#                 if(order.market_price > 0):
#                     data_item = [order.symbol,order.volume, order.price, order.total_cost, order.market_price, order.current_profit, order.current_rate_profit]
#                     orders.append(data_item)
#         df = pd.DataFrame(list(orders), columns=['symbol','volume','price', 'total_cost', 'm_price','profit','%'])
#         return df

#     @property
#     def total_buy_money(self):        
#         return np.sum(self.get_stocks_buy_orders['total_cost'])
#     @property
#     def total_profit(self):
#         return np.sum(self.get_stocks_buy_orders['profit'])
#     @property
#     def total_cost(self):
#         return np.sum(self.get_stocks_buy_orders['total_cost'])

#     def to_views(self, symbol):
#         df_view = self.get_stocks_buy_orders(symbol=symbol.upper())
#         #df_view = df_view[['symbol','volume','price', 'm_price','profit','%']]
        
#         #df_view['Note'] = df_view['%'].map(lambda x: self.notes(float(x)))

#         rs = []
#         for i in range(0,len(df_view)):
#             item = df_view.iloc[i]
#             symbol = item['symbol']
#             volume = item['volume']
#             price = item['price']
#             m_price = item['m_price']
#             _profit = item['profit']
#             rate_profit = item['%']

#             max_price = float(get_now_full_price(symbol=symbol)[1])
#             min_price = float(get_now_full_price(symbol=symbol)[2])
#             max_profit = profit(price,max_price)
#             min_profit = profit(price,min_price)

#             rs.append([symbol,volume,price,m_price,_profit, rate_profit, max_price,max_profit,min_price,min_profit])

#         df = pd.DataFrame(list(rs),columns=['symbol','volume','price', 'm_price','profit','%','max_price','max_%','min_price','min_%'])
#         df['volume'] = (df['volume']).map('{:,.0f}'.format)
#         df['price'] = (df['price']/1000).map('{:,.2f}'.format)
#         df['m_price'] = df['symbol'].map(lambda x: get_now_price(x)) # (df_view['m_price']/1000).map('{:,.2f}'.format)
#         df['m_price'] = (df['m_price']/1000).map('{:,.2f}'.format)
#         df['profit'] = (df['profit']).map(lambda x:RichNumber(float(x)).toText())
#         df['%'] = df['%'].map('{:,.2f}'.format)        
#         output = df.to_markdown()
#         output += f'\n Tổng vốn: {self.total_cost} | Tổng lợi nhuận: {self.total_profit} ({(self.total_profit/self.total_cost)*100:,.2f} (%))'
#         return output

# t = TeleViewer()
# print(t.to_views(symbol='HAX'))