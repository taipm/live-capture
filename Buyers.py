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
        self.length_data = len(self.stock.df_data)
        self.day_data = DayData(symbol=self.symbol,index=0,df_all_data=self.stock.df_data,count_days=10)
        #self.limit_days = 120

    def test_buy_FL(self):
        points = []
        count_FL = 0
        stop_print = False
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=3)
            max_price = np.max(day.df_next_data[2:]['Close'])
            min_price = np.min(day.df_next_data[2:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.isFL:
                if(not stop_print and not day.df_next_data.empty):
                    print(f'{day.price} | {day.index}' )
                    print(day.df_next_data[['Close','%']].to_markdown())
                    stop_print = True
                count_FL += 1
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
        print(f'{self.symbol} : FL - KL: {self.analysis_df_result(df):,.0f} (%)')
        return df
    
    def test_buy_CE(self):
        points = []
        count_FL = 0
        stop_print = False
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=3)
            max_price = np.max(day.df_next_data[2:]['Close'])
            min_price = np.min(day.df_next_data[2:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.isCE:
                if(not stop_print and not day.df_next_data.empty):
                    print(f'{day.price} | {day.index}' )
                    print(day.df_next_data[['Close','%']].to_markdown())
                    stop_print = True
                count_FL += 1
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
        print(f'{self.symbol} : CE - KL: {self.analysis_df_result(df):,.0f} (%)')
        return df
    
    def in_range(self, a,x,pct):
        min = inc_percent(x,-pct)
        max = inc_percent(x,pct)
        #print(f'range: {min} - {max}')
        if(a >= min and a <= max):
            return True
        else:
            return False
    
    def buy_with_pct(self, pct):
        points = []
        count_FL = 0
        stop_print = False
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=10)
            max_price = np.max(day.df_next_data[2:]['Close'])
            min_price = np.min(day.df_next_data[2:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.margin_price == pct:
                if(not stop_print and not day.df_next_data.empty):
                    print(f'{day.price} | {day.index}' )
                    print(day.df_next_data[['Close','%']].to_markdown())
                    stop_print = True
                count_FL += 1
                try:
                    _profit_max = profit(day.price,max_price)
                    _profit_min = profit(day.price,min_price)

                    note = f'M: {day.price} - B: {max_price} | LN (max) {_profit_max:,.2f} LN (min) {_profit_min:,.2f} (%)'
                    print(note)
                except:
                    print('Còn hơi sớm, chưa tới 10 phiên tiếp theo')
                points.append([day.index,day.price,day.margin_price,day.date,max_price,_profit_max,_profit_min,note])

        df = pd.DataFrame(list(points),columns=['i','price','%','day','max_p','LN-Max','LN-Min','Note'])
        df['LN-Max'] = df['LN-Max'].map('{:,.2f}'.format)
        df['LN-Min'] = df['LN-Min'].map('{:,.2f}'.format)
        print(f'{self.symbol} : {pct} - KL: {self.analysis_df_result(df):,.0f} (%)')
        return df

    def buy_with_range_pct(self, pct, range_pct):
        points = []
        count_FL = 0
        stop_print = False
        
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=10)
            
            _profit_max = None
            _profit_min = None
            note = ''

            if self.in_range(a = day.margin_price, x=pct,  pct=range_pct):
                #print(f'Phiên: index {day.index} : {day.index -2} | {day.index-day.T_days}')
                max_price = np.max(day.df_next_data[:day.T_days-2]['Close'])
                min_price = np.min(day.df_next_data[:day.T_days-2]['Close'])
                if(not stop_print and not day.df_next_data.empty):
                    #print(f'{day.price} | {day.index}' )
                    #print(day.df_next_data[['Close','%']].to_markdown())
                    #print(day.df_next_data[:day.T_days-2])
                    stop_print = True
                count_FL += 1
                try:
                    _profit_max = profit(day.price,max_price)
                    _profit_min = profit(day.price,min_price)
                    note = f'-M: {day.price} - B: {max_price} | LN (max) {_profit_max:,.2f} LN (min) {_profit_min:,.2f} (%)'
                    if(_profit_min >= 0):
                        note += ' : Tuyệt đối'
                    else:
                        note += f' : Cơ hội: {_profit_max + _profit_min:,.2f}'
                    #print(note)
                except:
                    print('Còn hơi sớm, chưa tới 10 phiên tiếp theo')
                points.append([day.index,day.price,day.margin_price,day.date,max_price,_profit_max,_profit_min,note])

        df = pd.DataFrame(list(points),columns=['i','price','%','day','max_p','LN-Max','LN-Min','Note'])
        df['LN-Max'] = df['LN-Max'].map('{:,.2f}'.format)
        df['LN-Min'] = df['LN-Min'].map('{:,.2f}'.format)
        min_pct = inc_percent(pct,-range_pct)
        max_pct = inc_percent(pct,range_pct)
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        if rate >= 70 and count_win >= 2:
            print(f'{self.symbol} : {pct} (%) [{min_pct} -> {max_pct}] - KL: {rate:,.0f} (%)')
        return df

    def test_buy_min_price(self):
        points = []
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=5)
            max_price = np.max(day.df_next_data[3:]['Close'])
            min_price = np.min(day.df_next_data[3:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.is_min_price:
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
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=10)
            print(f'Hiện tại: {i}')
            print(day.df_next_data)
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
        for i in range(0,self.length_data):
            
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=10)
            
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
        rate = 0
        if(count_win >= 2):
            print(f'{self.symbol} : Win {count_win} - Loss {count_lost}')
        if(count_win == 0):
            rate = 0
        elif count_lost == 0:
            rate = 100
        else:            
            rate = (count_win/(count_win + count_lost))*100
        return rate, count_win, count_lost, count_lost + count_lost

    def rateOfWin(self, margin_price):
        df_result = self.test_buy_isUpPrice(x=margin_price)
        y = self.analysis_df_result(df_result)
        return y

    def summary(self):
        output = f'\n{self.symbol} - Price Action\n'
        output += f'{self.stock.last_pct_price:,.2f} (%) - Rate win: {self.rateOfWin(self.stock.last_pct_price):,.2f} (%)'
        items = [6,5,4,3,2,1,-1,-2,-3,-4,-5,-6,-7]
        for item in items:
            up = item #%
            df_result = self.test_buy_isUpPrice(x=up)
            y = self.analysis_df_result(df_result)

            df_result = self.test_buy_isUpPriceAndVol(pct_price=up, pct_vol=up)
            x = self.analysis_df_result(df_result)
            output += f'\n{up}(%) - Win: {y:,.0f} (%): (+Vol): {x:,.0f} (%)'
        return output
    # def make_transactions(self):
    #     for p in self.get_buy_points():
    #         b = BuyOrder(symbol=self.symbol,volume=100,price=p)

# stocks = ['FRT','HBC','VND','KBC','SCR','TCB','BID','TPB','MSH','VGI','DXG','HAX','NVL']
# stocks = ['BSI','HAH','ASM','DGC','DPM','DXG','FRT','HAX','HBC','HPG','MSH','MWG','NLG','PDR','SCR','SSI','SZC','VND','BID','TPB','MWG'] #'IDC'
# stocks = list(set(stocks))
stocks = ['VGI','VND','FPT', 'HAX','SCR','DXG','SSI','BSI']
items = [6,5,4,3,2,1,-1,-2,-3,-4,-5,-6,-7]
for s in stocks:
    f = Buyer(symbol=s)
    #f.buy_with_pct(1.53)
    for pct in items:
        f.buy_with_range_pct(pct=pct, range_pct=2) #Biến động 1%
    #df = f.test_buy_FL()
    #print(df.to_markdown())
    #df = f.test_buy_CE()
    #print(df.to_markdown())
    #print(f.summary())