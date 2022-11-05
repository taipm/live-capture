from Caculator import *
from DayData import * #DateStick, DayData
from CandleStick import CandleStick
from IntradayData import *
import db
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import datetime as dt
from vnstock import *
from Pivot import *

# sns.set()
# pd.options.display.float_format='{:,.2f}'.format
# pd.set_option('display.width',85)

class Stock:
    def __init__(self, name) -> None:
        self.name = name.upper()
        #self.df_data = pd.DataFrame()
        self.StrSummary = self.name
        self.FileName = ''
 
        self.df_data = self.Load_Daily_Data()
        self.len = len(self.df_data)
        #self.df_daily_data = self.df_data
        self.last_price = self.df_data['Close'][0]
        self.last_volume = self.df_data['Volume'][0]
        
        self.daily_prices = self.df_data['Close']
        self.daily_volumes = self.df_data['Volume']
        self.daily_foreign = self.df_data['NN']
        self.daily_money = self.df_data['Money']
        self.daily_low_prices = self.df_data['Low']
        self.daily_high_prices = self.df_data['High']
        self.daily_open_prices = self.df_data['Open']
        self.daily_close_prices = self.df_data['Close']

        #self.price = self.daily_prices[0]
        self.max_price = np.max(self.daily_prices)
        self.min_price = np.min(self.daily_prices)
        self.vol = self.daily_volumes[0]
        self.max_vol = np.max(self.daily_volumes)
        self.min_vol = np.min(self.daily_volumes)
        self.avg_vol = np.average(self.daily_volumes)

        self.TCB_Data = self.load_basic_data()#price_board(self.name)
        #print(self.TCB_Data.transpose())
        self.intraday_price = self.TCB_Data['Giá Khớp Lệnh'].values[0]/1000
        self.TCB_valuation = self.TCB_Data['TCBS định giá'].values[0]/1000
        self.max_price_year = self.TCB_Data['Đỉnh 1Y'].values[0]/1000
        self.min_price_year = self.TCB_Data['Đáy 1Y'].values[0]/1000
        self.MA20 = self.TCB_Data['MA20'].values[0]/1000
        self.MA50 = self.TCB_Data['MA50'].values[0]/1000
        self.MA100 = self.TCB_Data['MA100'].values[0]/1000
        self.RSI = self.TCB_Data['RSI'].values[0]
        self.PB = self.TCB_Data['P/B'].values[0]
        self.PE = self.TCB_Data['P/E'].values[0]
        self.ROE = self.TCB_Data['ROE'].values[0]*100

        self.STICKS = self.ToCandleSticks()
        #self.df_intraday_data = self.load_intraday_data()
    
    def Load_Daily_Data(self) -> pd.DataFrame:
        return db.GetStockData(self.name)

    @property
    def price(self):
        if(self.intraday_price != self.daily_prices[0]):
            return self.intraday_price
        else:
            return self.daily_prices[0]
    @property
    def review_price(self):
        output = f''
        if(self.price >= self.max_price_year):
            output += f'Vượt đỉnh năm: {percent(self.price,self.max_price_year):,.2f} (%)'
        elif(self.price <= self.min_price_year):
            output += f'Thủng dáy năm: {percent(self.price,self.min_price_year):,.2f} (%)'
        else:
            output += f'Chưa có gì đặc biệt'
        return output
    @property
    def review_candle_stick(self):
        stick = self.STICKS[0]
        return stick.Get_Summary()
    @property
    def review_ROE(self):
        output = f'ROE = {self.ROE:,.2f}'
        if self.ROE <= 10:
            output += f': Quá thấp'
        elif self.ROE >= 15 and self.ROE < 20:
            output += f': Hợp lý'
        elif self.ROE >= 20:
            output += f': Hấp dẫn'
        return output

    @property
    def review_PB(self):
        output = f'PB = {self.PB:,.2f}'
        if self.PB <= 1:
            output += f': Hấp dẫn'
        elif self.PB >= 2 and self.PB < 3:
            output += f': Hợp lý'
        elif self.PB >= 3:
            output += f': Quá cao'
        return output
    
    @property
    def review_RSI(self):
        output = f'RSI = {self.RSI:,.2f}'
        if self.RSI <= 30:
            output += f': Quá bán'
        if self.RSI <= 35 and self.RSI > 30:
            output += f': Gần quá bán'
        elif self.RSI >= 90:
            output += f': Quá mua'
        elif self.RSI >= 70 and self.RSI <= 85:
            output += f': Đang năng động'
        return output

    @property
    def review_TCB_valuation(self):
        valuation = self.TCB_valuation
        output = f'Giá: {self.price:,.2f} - Định giá: {valuation:,.2f} | Tỷ lệ: {self.price/valuation:,.2f} (%)'
        if(self.price <= valuation):
            output += ' => Hấp dẫn'
        else:
            output += ' => Cao, xem lại'
        return output

    @property
    def review(self):
        output = f'Nhận xét (cơ bản) :'+\
            f'\n- {self.review_ROE}' +\
            f'\n- {self.review_RSI}' +\
            f'\n- {self.review_PB}' +\
            f'\n- {self.review_TCB_valuation}'
        return output

    def load_basic_data(self):
        return price_board(self.name)

    def get_percent_price(self, index):
        if(index < 0):
            return None
        return self.df_data['%'][index]

    def get_percent_vol_day(self):
        return percent(self.daily_volumes[0], self.daily_volumes[1])
    
    def get_percent_vol_avg_week(self, index):
        start = index
        end = index + 5
        vol_avg_week = np.average(self.df_data['Volume'][start:end])
        return percent(self.df_data['Volume'][0], vol_avg_week)

    def get_percent_vol_avg_10days(self, index):
        start = index
        end = index + 10
        vol_avg_week = np.average(self.df_data['Volume'][start:end])
        return percent(self.df_data['Volume'][0], vol_avg_week)

    def get_percent_vol_avg_month(self, index):
        start = index
        end = index + 20
        vol_avg_week = np.average(self.df_data['Volume'][start:end])
        return percent(self.df_data['Volume'][0], vol_avg_week)

    def is_min_vol(self,index):
        vol = self.df_data.iloc[index]['Volume']
        rate_of_profit = self.get_profit_by_index(index=index,pre_count_of_days=-1)
        if(vol <= self.avg_vol and rate_of_profit <= 2 and rate_of_profit >= -3):
            return True
        else:
            return False

    def is_pivot_point(self,index):
        rate_of_price = 2
        rate_of_vol = 1.2
        time_to_check = 10

        if(self.get_percent_price(index=index)>=rate_of_price):
            if(self.df_data['Close'][index] > self.df_data['Open'][index]):
                if(self.df_data['Volume'][index] > np.max(self.df_data['Volume'][index+1:index+time_to_check])):
                    if(self.get_percent_vol_avg_10days(index=index)>=rate_of_vol):
                        return True

    def get_pivots(self):
        pivots = []
        start = 0
        end = len(self.df_data)-20
        for i in range(start,end):
            if self.is_pivot_point(i):
                p = Pivot(symbol=self.name,index=i)
                pivots.append(p)
        return pivots

    def get_min_vols(self):
        results = []
        start = 0
        end = len(self.df_data)-20
        for i in range(start,end):
            if self.is_min_vol(i):
                p = Pivot(symbol=self.name,index=i)
                results.append(p)
        return results

    def get_data_by_index(self,index):
        data = self.df_data.iloc[index]
        return data

    def get_profit_by_index(self,index, pre_count_of_days):
        price = self.df_data.iloc[index]['Close']
        n_price = self.df_data.iloc[index-pre_count_of_days]['Close']
        return percent(price,n_price)
    
    def check_profit(self,index):
        values = []
        price = self.df_data.iloc[index]['Close']
        pre_count_of_days = 10
        for i in range(0,pre_count_of_days):
            n_price = self.df_data.iloc[index-i]['Close']
            profit = percent(price,n_price)
            values.append(profit)
        return np.max(values),np.min(values)

    def get_pivots_as_string(self):
        start = 0
        end = len(self.df_data)-20
        output = ''
        for i in range(start,end):
            if self.is_pivot_point(i):
                if(i <= 30):
                    output += f'\n{i} - Pivot {self.daily_prices[i]} - {self.df_data["%"][i]}'
        if(len(output)>1):
            output = f'\nPivots:\n' + output
        return output
        
    def Get_Price(self, d_str):
        item = self.df_data[self.df_data['Date'] == dt.datetime.strptime(d_str, '%Y-%m-%d').date()]
        return item['Close'].values
    
    def Get_Volume(self, d_str):
        item = self.df_data[self.df_data['Date'] == dt.datetime.strptime(d_str, '%Y-%m-%d').date()]
        return item['Volume'].values
    
    def GetDataItem(self, d_str):        
        item = self.df_data[self.df_data['Date'] == dt.datetime.strptime(d_str, '%Y-%m-%d').date()]
        return item
    
    def GetDataItemAtPrev(self,countOfPrevDays):
        item = self.df_data.iloc[countOfPrevDays]
        return item
    
    def GetPriceAtPrev(self,countOfPrevDays):
        return self.GetDataItemAtPrev(countOfPrevDays=countOfPrevDays)['Close']
    
    @property
    def last_trans_date(self):
        return self.df_data['Date'][0]

    def GetLastPrice(self):
        return self.df_data['Close'][0]

    def ToCandleSticks(self):
        sticks = list()
        for i in range(0,self.len):
            stick = CandleStick(high = self.df_data['High'][i],
                                close = self.df_data['Close'][i],
                                open = self.df_data['Open'][i],
                                low = self.df_data['Low'][i],
                                volume = self.df_data['Volume'][i],
                                index = i)
            sticks.append(stick)            
    
        return sticks
    
    @property
    def rate_of_waze(self):
        """
        Tỷ lệ sóng: Là số lần dao động cao trên khung thời gian
        - T: Là khung thời gian (số phiên)
        - percent: Tỷ lệ đo sóng (thường khoảng 3% trở lên được xem là dao động mạnh)
        Kết quả:
        -1: Là lỗi (vượt quá không gian dữ liệu)
        """
        T = 20
        percent = 3

        if(T > len(self.df_data)):
            return -1 #Lỗi
        #df = self.df_data[0:T] #Cắt dữ liệu cho khớp với số phiên
        sticks = self.STICKS[0:T] #Lấy số nến
        count_amp = 0 #Đếm biên độ dao động
        for stick in sticks:
            if np.abs(stick.Percent())>= percent:
                count_amp += 1
        
        return count_amp/T

    def Describe(self):
        output = f'{self.name} [{self.last_trans_date}] - {self.price}'
        output += f'\nNhận xét (giá): {self.review_price}'
        output += f'\nNhận xét (nến): {self.review_candle_stick}'
        output += f'\nKL cao nhất: {self.max_vol:,.0f} | KL thấp nhất: {self.min_vol:,.0f}'
        output += f'\nThanh khoản: {self.daily_money[0]:,.0f} | CN/TN: {np.max(self.daily_money):,.0f} | {np.min(self.daily_money):,.0f}'
        output += f'\n{self.review}'
        output += f'\n- Tỷ lệ sóng: {self.rate_of_waze:,.2f}'
        output += f'\n{"-"*30}'
        if(len(self.get_pivots()) > 0):
            output += f'\n{self.get_pivots_as_string()}'
        return output

stocks = ['KBC','BSI','SCR']
for s in stocks:
    s = Stock(name=s)
    #print(f'{s.name} - {s.rate_of_waze}')
    print(f'{s.Describe()}')
    # d = DayData(symbol=s.name, index=0,df_all_data=s.df_data,count_days=10)
    # print(d.get_info())

# stocks = ['KSB','TPB','VND','KBC','CEO','BID','CTG']
# for s in stocks:
#     s = Stock(name=s)
#     #s.check_pivots()
#     s.check_min_vol()



#print(s.get_profit_by_index(0,-1)) #so voi phien truoc (-1)
# print(s.get_profit_by_index(1,-1)) #so voi phien truoc (-1)
# print(s.get_profit_by_index(1,1)) #so voi phien sau (-1)

# path = s.draw()
# print(path)
# print(s.TCB_Suggest_Price)
# print(s.RSI)
# print(s.Price)
# print(s.df_weekly_data)
# # item = s.GetDataItemAtPrev(5).values
# # print(item)
# print(s.Describe())
# #p = s.GetPrice('2022-08-05')
#p = s.Get_Profit('2022-08-01','2022-08-05')
# print(p)
#s.DrawWithForcecast(N=30)
#print(s.StrSummary)