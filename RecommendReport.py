from DateData import DateData
from MongoDb import MongoDb
from Stock import Stock

class RecommendReport:
    def __init__(self) -> None:
        pass

    def getRecommends(self):
        db = MongoDb(name='Recommends')
        df = db.getAll()
        
        return df[['symbol','date_recommend']]
    
    def analysis(self):
        df = self.getRecommends()
        results = ''
        for i in range(len(df)):
            item = df.iloc[i]
            symbol = item['symbol']
            date = item['date_recommend'].split(' ')[0]
            stock = Stock(symbol)
            data_item = stock.getIndex(str_date=str(date))
            index = data_item.index.values[0]
            price = data_item['Close'].values[0]
            last_price = stock.price
            
            try:
                profit = ((last_price-price)/price)*100
                print(f'{symbol} - {index} - Giá : {price}: {profit}')
            except:
                print('Chưa đủ thời gian tính toán')
        return results


r = RecommendReport()
#df = r.getRecommends()
#print(df)
stocks = r.analysis()
# print(stocks)
# for symbol in stocks[0:2]:
#     stock1 = Stock(name = symbol)
#     #print(stock1.df_data)
#     #stock2 = DateData(symbol=symbol)
#     print(stock1.getIndex("2022-12-09"))