import datetime
from MongoDb import ObjectDb
from db import *

class Recommend(ObjectDb):
    def __init__(self, symbol:str, type_recommend:str, date_recommend:datetime) -> None:
        super().__init__()
        self.symbol = symbol
        self.type_recommend = type_recommend
        self.date_recommend = date_recommend

    def profit(self, next_days:int)->float:
        recommend_index = get_index_by_date(symbol = self.symbol, date=self.date_recommend)
        print(f'Recommend index: {recommend_index} : {self.date_recommend}')
        price = get_price_by_date(symbol = self.symbol, date=str(self.date_recommend))
        
        index = recommend_index - next_days
        next_price = get_price_by_index(symbol = self.symbol, index=index)
        
        profit = ((next_price-price)/price)*100
        print(f'{price} - {self.date_recommend} | {next_price} : {index} -> {profit}')
        
        return profit

# r = Recommend(symbol='BSR',type_recommend='MA-GIAO NHAU', date_recommend='2022-11-02 21:10:46.529476')
# print(f'{r.profit(next_days=10):,.2f} (%)')
