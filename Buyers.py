from DayData import DayData
from TextHelper import *
from DateHelper import *
from Stock import Stock
import pandas as pd
from StockOrder import *
import numpy as np

class Buyer:
    def __init__(self, symbol) -> None:
        self.name = 'Buyer'
        self.symbol = toStandard(symbol).upper()
        self.stock = Stock(name = self.symbol)
        self.day_data = DayData(symbol=self.symbol,index=0,df_all_data=self.stock.df_data,count_days=10)
        self.limit_days = 120

    def test_buy_FL(self):
        points = []
        for i in range(0,self.limit_days):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit_max = None
            _profit_min = None
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
        for i in range(0,self.limit_days):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit_max = None
            _profit_min = None
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
    
    def test_buy_min_price(self):
        points = []
        for i in range(0,self.limit_days):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.isMinPrice:
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

    def test_buy_isUp3(self):
        points = []
        for i in range(0,self.limit_days):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.isUp3:
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
        
    def test_buy_isUpPrice(self,x:float):
        points = []
        for i in range(0,self.limit_days):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.isUpPrice(x):
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

    def test_buy_isUpPriceAndVol(self,pct_price:float,pct_vol):
        points = []
        for i in range(0,self.limit_days):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.isUpPrice(pct_price) and day.isUpVolume(pct_vol):
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
        if(count_lost == 0):
            return 100
        else:
            #print(f'Lãi: {count_win} - Lỗ: {count_lost} | TL {(count_win/(count_win + count_lost))*100:,.2f} (%)')
            return (count_win/(count_win + count_lost))*100
    def summary(self):
        output = f'{self.symbol} - PP: Price Action\n'

        items = [6,5,4,3,2,1,-1,-2,-3,-4,-5,-6]
        for item in items:
            up = item #%

            df_result = self.test_buy_isUpPrice(x=up)
            y = self.analysis_df_result(df_result)

            df_result = self.test_buy_isUpPriceAndVol(pct_price=up, pct_vol=up)
            x = self.analysis_df_result(df_result)                        
            output += f'\n{up}(%) - Price: {y:,.2f} (%) : Price and Vol: {x:,.2f} (%)'
        return output
    # def make_transactions(self):
    #     for p in self.get_buy_points():
    #         b = BuyOrder(symbol=self.symbol,volume=100,price=p)

# stocks = ['FRT','HBC','VND','KBC','SCR','TCB','BID','TPB','MSH','VGI','DXG','HAX','NVL']
# stocks = ['BSI','HAH','ASM','DGC','DPM','DXG','FRT','HAX','HBC','HPG','MSH','MWG','NLG','PDR','SCR','SSI','SZC','VND','BID','TPB','MWG'] #'IDC'
# stocks = list(set(stocks))
# stocks = ['VND']
# for s in stocks:
#     f = Buyer(symbol=s)
#     print(f.summary())