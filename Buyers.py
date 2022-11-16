from DayData import DayData
from TextHelper import *
from DateHelper import *
from Stock import Stock
import pandas as pd
from SellOrder import *
import numpy as np

class Buyer:
    def __init__(self, symbol) -> None:
        self.name = 'Buyer'
        self.symbol = toStandard(symbol).upper()
        self.stock = Stock(name = self.symbol)
        self.pct_price = self.stock.last_pct_price
        self.df_data = self.stock.df_data#[0:20]
        self.length_data = len(self.df_data)
        self.day_data = DayData(symbol=self.symbol,index=0,df_all_data=self.df_data,count_days=10)
        #self.limit_days = 120

    def buy_supper_volume(self):
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

            if day.is_supper_volume(4):
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
        
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        #print(f'count: {count_FL}')
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'Supper-volume (3) ~ {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'

        return df, output

    def buy_breakVol(self):
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

            if day.is_break_volume(3):
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
        
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        #print(f'count: {count_FL}')
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'Break vol(3) ~ {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'

        return df, output

    def buy_breakVol_price(self,pct_price):
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

            if day.is_max_vol and day.margin_price >= pct_price:
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
        
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        #print(f'count: {count_FL}')
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'Max(vol,price>={pct_price:,.2f}) ~ {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'

        return df, output
    '''
    '''

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
        
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        #print(f'count: {count_FL}')
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'FL ~ {rate_in_range:,.2f}(%) | số phiên thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'

        return df, output
    
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
        
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'CE ~ {rate_in_range:,.2f}(%) | số phiên thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'

        return df, output
        
    def in_range(self, a,x,pct):
        min = None
        max = None
        if (x >= 0):
            min = inc_percent(x,-pct)
            max = inc_percent(x,pct)
        else:
            min = inc_percent(x,pct)
            max = inc_percent(x,-pct)
        if(a >= min and a <= max):
            return True
        else:
            return False
    def buy_with_max_price(self): #Giá vượt đỉnh
        points = []
        count_FL = 0
        stop_print = False
        count_days = 10
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=count_days)
            max_price = np.max(day.df_next_data[2:]['Close'])
            min_price = np.min(day.df_next_data[2:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.is_max_price:
                count_FL += 1
                try:
                    _profit_max = profit(day.price,max_price)
                    _profit_min = profit(day.price,min_price)

                    note = f'M: {day.price} - B: {max_price} | LN (max) {_profit_max:,.2f} LN (min) {_profit_min:,.2f} (%)'
                    #print(note)
                except:
                    print('Còn hơi sớm, chưa tới 10 phiên tiếp theo')
                points.append([day.index,day.price,day.margin_price,day.date,max_price,_profit_max,_profit_min,note])

        df = pd.DataFrame(list(points),columns=['i','price','%','day','max_p','LN-Max','LN-Min','Note'])
        df['LN-Max'] = df['LN-Max'].map('{:,.2f}'.format)
        df['LN-Min'] = df['LN-Min'].map('{:,.2f}'.format)
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        #print(f'count: {count_FL}')
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'Đỉnh {count_days} phiên ~ rate in range: {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'
        # if rate >= 70 and count_win >= 2:
        #     print(f'{self.symbol} : {pct}(%) ~ rate in range: {rate_in_range:,.2f}(%) [{min_pct} -> {max_pct}] số phiên thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)')
        return df, output
    def buy_with_min_price(self): #Giá vượt đỉnh
        points = []
        count_FL = 0
        stop_print = False
        count_days = 10
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=count_days)
            max_price = np.max(day.df_next_data[2:]['Close'])
            min_price = np.min(day.df_next_data[2:]['Close'])
            _profit_max = None
            _profit_min = None
            note = ''
            if day.is_max_price:
                count_FL += 1
                try:
                    _profit_max = profit(day.price,max_price)
                    _profit_min = profit(day.price,min_price)

                    note = f'M: {day.price} - B: {max_price} | LN (max) {_profit_max:,.2f} LN (min) {_profit_min:,.2f} (%)'
                    #print(note)
                except:
                    print('Còn hơi sớm, chưa tới 10 phiên tiếp theo')
                points.append([day.index,day.price,day.margin_price,day.date,max_price,_profit_max,_profit_min,note])

        df = pd.DataFrame(list(points),columns=['i','price','%','day','max_p','LN-Max','LN-Min','Note'])
        df['LN-Max'] = df['LN-Max'].map('{:,.2f}'.format)
        df['LN-Min'] = df['LN-Min'].map('{:,.2f}'.format)
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        #print(f'count: {count_FL}')
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'Đáy {count_days} phiên ~ rate in range: {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - TL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'
        # if rate >= 70 and count_win >= 2:
        #     print(f'{self.symbol} : {pct}(%) ~ rate in range: {rate_in_range:,.2f}(%) [{min_pct} -> {max_pct}] số phiên thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)')
        return df, output
    def buy_with_current_pct(self):
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
            if day.margin_price == self.pct_price:
                count_FL += 1
                try:
                    _profit_max = profit(day.price,max_price)
                    _profit_min = profit(day.price,min_price)

                    note = f'M: {day.price} - B: {max_price} | LN (max) {_profit_max:,.2f} LN (min) {_profit_min:,.2f} (%)'
                    #print(note)
                except:
                    print('Còn hơi sớm, chưa tới 10 phiên tiếp theo')
                points.append([day.index,day.price,day.margin_price,day.date,max_price,_profit_max,_profit_min,note])

        df = pd.DataFrame(list(points),columns=['i','price','%','day','max_p','LN-Max','LN-Min','Note'])
        df['LN-Max'] = df['LN-Max'].map('{:,.2f}'.format)
        df['LN-Min'] = df['LN-Min'].map('{:,.2f}'.format)
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        #print(f'count: {count_FL}')
        rate_in_range = (count_FL/self.length_data)*100
        output = f'Hiện tại {self.pct_price:,.2f}(%) ~ rate in range: {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - KL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'
        return df, output

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
                count_FL += 1
                max_price = np.max(day.df_next_data[:day.T_days-2]['Close'])
                min_price = np.min(day.df_next_data[:day.T_days-2]['Close'])
                
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
        count_lost = rs[2]
        sum_count = rs[3]
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'{pct}(%) - Vùng biến động: [{min_pct:,.2f} -> {max_pct:,.2f}]  ~ rate in range: {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - TL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'
        return df, output

    def buy_with_highest(self):
        points = []
        count_FL = 0
        stop_print = False
        
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=10)
            
            _profit_max = None
            _profit_min = None
            note = ''

            if day.is_highest_price:
                count_FL += 1
                max_price = np.max(day.df_next_data[:day.T_days-2]['Close'])
                min_price = np.min(day.df_next_data[:day.T_days-2]['Close'])
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
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        rate_in_range = (count_FL/self.length_data)*100
        
        output = f'Close=High (highest) ~ {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - TL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'
        return df, output

    def buy_with_lowest(self):
        points = []
        count_FL = 0
        stop_print = False
        
        for i in range(0,self.length_data):
            day = DayData(symbol=self.symbol,index=i,df_all_data=self.stock.df_data,count_days=10)
            
            _profit_max = None
            _profit_min = None
            note = ''

            if day.is_lowest_price:
                count_FL += 1
                max_price = np.max(day.df_next_data[:day.T_days-2]['Close'])
                min_price = np.min(day.df_next_data[:day.T_days-2]['Close'])
                
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
        rs = self.analysis_df_result(df)
        rate = rs[0]
        count_win = rs[1]
        count_lost = rs[2]
        sum_count = rs[3]
        rate_in_range = (count_FL/self.length_data)*100
        output = f'Close=Low (Lowest) ~ {rate_in_range:,.2f}(%) | Thắng {count_win}/{sum_count} - TL: {rate:,.0f} (%)'
        if(rate <= 50):
            output += ': Nguy hiểm -> Bán'
        elif(rate>=70):
            output += ': Cơ hội -> Mua'
        else:
            output += ': Theo dõi'
        return df, output

    
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
        df['Win'] = df['LN-Max'].map(lambda x: float(x)>=3)# and df['LN-Min'].map(lambda x:float(x)>=-3)
        count_win = len(df[df['Win']==True])
        count_lost = len(df[df['Win']!=True])
        rate = 0
        if(count_win == 0):
            rate = 0
        elif count_lost == 0 and count_win == 0:
            rate = 0
        elif count_lost == 0 and count_win > 0:
            rate = 100
        else:
            rate = (count_win/(count_win + count_lost))*100
        return rate, count_win, count_lost, count_win + count_lost

    def rateOfWin(self, margin_price):
        df_result = self.test_buy_isUpPrice(x=margin_price)
        y = self.analysis_df_result(df_result)
        return y

    def to_string(self):
        output = f'{self.symbol} - Tổng số phiên: {self.length_data}\n'
        return output

    def summary(self):
        output = f'\n{self.symbol} - Tính toán & dự báo | {self.length_data} (phiên)\n'
        output += f'\n {self.buy_with_current_pct()[1]}'
        output += f'\n {self.buy_with_range_pct(pct=self.pct_price,range_pct=9)[1]}' #9% của pct_price
        output += f'\n {self.test_buy_CE()[1]}'
        output += f'\n {self.test_buy_FL()[1]}'
        output += f'\n {self.buy_with_highest()[1]}'
        output += f'\n {self.buy_with_lowest()[1]}'
        output += f'\n {self.buy_with_max_price()[1]}'
        output += f'\n {self.buy_breakVol()[1]}'
        output += f'\n {self.buy_breakVol_price(pct_price = 3)[1]}'
        output += f'\n {self.buy_supper_volume()[1]}'
        output += f'\n{"-"*20}'
        return output

# stocks = ['FRT','HBC','VND','KBC','SCR','TCB','BID','TPB','MSH','VGI','DXG','HAX','NVL']
# stocks = ['BSI','HAH','ASM','DGC','DPM','DXG','FRT','HAX','HBC','HPG','MSH','MWG','NLG','PDR','SCR','SSI','SZC','VND','BID','TPB','MWG'] #'IDC'

# stocks = ['VGI','VND','FPT', 'HAX','SCR','DXG','SSI','BSI','HBC','MSH','MWG','PVT']
# stocks = list(set(stocks))
# for s in stocks:
#   b = Buyer(symbol=s)
#   print(b.summary())


# b = Buyer(symbol='HAX')
# print(b.summary())