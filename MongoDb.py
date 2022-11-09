#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from pymongo import MongoClient, message
from pprint import pprint
import pandas as pd
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from StockOrder import *

class MongoDb:
    def __init__(self) -> None:
        client = MongoClient("mongodb+srv://taipm:mNIZQSFNRm4XMLhs@cluster0.nskndlz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        self.db = client['TradingBook']
        self.collections = self.db.list_collection_names()

    def to_string(self):        
        print(f'{self.db.name}')
        print(f'{self.collections}')

        #print(self.Orders)

class OrderDb(MongoDb):
    def __init__(self) -> None:
        super().__init__()
        self.Orders = self.db.get_collection('Orders')
        self.df_data = self.getOrders()
            
    def addOder(self, order):
        self.Orders.insert_one(json.loads(order))

    def getOrders(self):
        orders = self.Orders.find()        
        df =  pd.DataFrame(list(orders))
        return df
    
    def getStockOrders(self, symbol):
        return self.Orders.find({'symbol':symbol})
    
    def getOrder(self, query):
        return self.Orders.find_one(query)

    def print_data(self):
        print(self.getOrders())

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
        print(f'Tổng lệnh: {self.orders}')
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
# db.to_string()


