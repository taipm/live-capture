from DayData import DayData
from TextHelper import *
from DateHelper import *
from Stock import Stock
import pandas as pd
from StockOrder import *
import numpy as np

class Buyer:
    def __init__(self, symbol) -> None:
        self.name = 'Buy with FL'
        self.symbol = toStandard(symbol).upper()
        self.stock = Stock(name = self.symbol)
        # self.df = self.stock.df_data
        # self.last_price = self.stock.price
        # self.last_margin = self.stock.la
        self.day_data = DayData(symbol=self.symbol,index=0,df_all_data=self.stock.df_data,count_days=10)

    def isFL(self):
        if(self.day_data.isFL):
            return True
        else:
            return False
    def isCE(self):
        if(self.day_data.isCE):
            return True
        else:
            return False
    # def test_buy_FL(self):

    def test_buy_FL(self):
        points = []
        for i in range(0,400):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit = None
            note = ''
            if day.isFL:
                try:
                    _profit_max = profit(day.price,max_price)
                    _profit_min = profit(day.price,min_price)

                    note = f'M: {day.price} - B: {max_price} | LN (max) {_profit_max:,.2f} LN (min) {_profit_min:,.2f} (%)'
                except:
                    print('Còn hơi sớm, chưa tới 10 phiên tiếp theo')
                points.append([day.index,day.price,day.margin_price,day.date,max_price,_profit_max,_profit_min,note])

        df = pd.DataFrame(list(points),columns=['i','price','%','day','max_p','LN-Max','LN-Min','Note'])
        df['LN-Max'] = df['LN-Max'].map('{:,.2f}'.format)
        df['LN-Min'] = df['LN-Min'].map('{:,.2f}'.format)
        return df
    
    def test_buy_CE(self):
        points = []
        for i in range(0,400):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit = None
            note = ''
            if day.isCE:
                try:
                    _profit_max = profit(day.price,max_price)
                    _profit_min = profit(day.price,min_price)

                    note = f'M: {day.price} - B: {max_price} | LN (max) {_profit_max:,.2f} LN (min) {_profit_min:,.2f} (%)'
                except:
                    print('Còn hơi sớm, chưa tới 10 phiên tiếp theo')
                points.append([day.index,day.price,day.margin_price,day.date,max_price,_profit_max,_profit_min,note])

        df = pd.DataFrame(list(points),columns=['i','price','%','day','max_p','LN-Max','LN-Min','Note'])
        df['LN-Max'] = df['LN-Max'].map('{:,.2f}'.format)
        df['LN-Min'] = df['LN-Min'].map('{:,.2f}'.format)
        return df
    
    def analysis_df_result(self,df:pd.DataFrame):
        df['LN-Max'] = df['LN-Max'].map(lambda x:float(x))
        df['LN-Min'] = df['LN-Min'].map(lambda x:float(x))
        count_win = len(df[df['LN-Max']>=0])
        count_lost = len(df[df['LN-Max']<0])
        print(f'Lãi: {count_win} - Lỗ: {count_lost} | TL {(count_win/(count_win + count_lost))*100:,.2f} (%)')
    # def make_transactions(self):
    #     for p in self.get_buy_points():
    #         b = BuyOrder(symbol=self.symbol,volume=100,price=p)

stocks = ['FRT','HBC','VND','KBC','SCR','TCB','BID','TPB']
for s in stocks:
    f = Buyer(symbol=s)

    print(s + ' : MUA SÀN')
    df_result = f.test_buy_FL()
    #print(df_result.to_markdown())
    f.analysis_df_result(df_result)

    print(s + ' : MUA TRẦN')
    df_result = f.test_buy_CE()
    #print(df_result.to_markdown())
    f.analysis_df_result(df_result)

class BuyerCE:
    def __init__(self) -> None:
        self.name = 'Buy with CE'

class BuyerPivot:
    def __init__(self) -> None:
        self.name = 'Buy with Pivot (vol, price)'

class BuyerMinVol:
    def __init__(self) -> None:
        self.name = 'Buy with min vol'
