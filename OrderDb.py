import json
from DateHelper import isToday
from MongoDb import MongoDb
import pandas as pd

class OrderDb(MongoDb):
    def __init__(self) -> None:
        super().__init__()
        self.Orders = self.db.get_collection('Orders')
        self.df_data = self.getOrders()
        self.count_orders = len(self.df_data)
            
    def addOder(self, order):
        self.Orders.insert_one(json.loads(order))

    def getOrders(self):
        orders = self.Orders.find()        
        df =  pd.DataFrame(list(orders))
        return df
    
    def getStockOrders(self, symbol):
        orders = self.Orders.find({'symbol':symbol})
        df =  pd.DataFrame(list(orders))
        df = df.sort_values(by=['time'])
        return df

    def getStockOrdersByToday(self):
        df = self.df_data
        df = df[df['time'].map(lambda x: isToday(x)==True)]
        df = df.sort_values(by=['time'])
        return df

    def getOrder(self, query):
        return self.Orders.find_one(query)

    def __str__(self):
        return self.getOrders()


class TransactionDb(MongoDb):
    def __init__(self) -> None:
        super().__init__()
        self.items = self.db.get_collection('Transactions')
        self.df_data = self.get_all()
    
    def add_item(self, item):
        self.items.insert_one(json.loads(item))

    def get_all(self):
        items = self.items.find()        
        df =  pd.DataFrame(list(items))
        return df