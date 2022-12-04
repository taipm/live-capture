import datetime
from MongoDb import ObjectDb
from db import *

class Recommend(ObjectDb):
    def __init__(self, symbol:str, type_recommend:str, date_recommend:datetime) -> None:
        super().__init__()
        self.symbol = symbol
        self.type_recommend = type_recommend
        self.date_recommend = date_recommend

    def profit(self, window:int)->float:
        price = get_price_by_date(symbol = self.symbol, date=str(self.date_recommend))
        next_price = get_price_by_date(symbol = self.symbol, date='2022-12-02 21:10:46.529476')
        return ((next_price-price)/price)*100

r = Recommend(symbol='BSR',type_recommend='MA-GIAO NHAU', date_recommend='2022-11-02 21:10:46.529476')
print(f'{r.profit(window=10):,.2f} (%)')
