from Caculator import *
from DayData import * #DateStick, DayData
from IntradayData import *
from PriceAction import PriceAction
import db
import pandas as pd
import numpy as np
import datetime as dt
from vnstock import *

class Stock:
    def __init__(self, name) -> None:
        self.name = name.upper()
        self.StrSummary = self.name
        self.FileName = ''
 
        self.df_data = self.Load_Daily_Data()
        self.len = len(self.df_data)
        
        self.last_price = self.df_data['Close'][0]
        self.last_volume = self.df_data['Volume'][0]
        self.last_pct_price = self.df_data['%'][0]
        
        self.prices = self.df_data['Close']
        self.daily_volumes = self.df_data['Volume']
        self.daily_foreign = self.df_data['NN']
        self.daily_money = self.df_data['Money']
        self.daily_low_prices = self.df_data['Low']
        self.daily_high_prices = self.df_data['High']
        self.daily_open_prices = self.df_data['Open']
        self.daily_close_prices = self.df_data['Close']

        self.max_price = np.max(self.prices)
        self.min_price = np.min(self.prices)
        self.vol = self.daily_volumes[0]
        self.max_vol = np.max(self.daily_volumes)
        self.min_vol = np.min(self.daily_volumes)
        self.avg_vol = np.average(self.daily_volumes)
        self.TCB_Data = self.load_basic_data()
        #print(self.TCB_Data.transpose())
        try:        
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

            self.signal_KT = self.TCB_Data['Tín hiệu KT'].values[0]
            self.signal_TBD = self.TCB_Data['Tín hiệu TB động'].values[0]
            self.MACD_Signal = self.TCB_Data['MACD Signal'].values[0]
            self.MACD_Volume = self.TCB_Data['MACD Volume'].values[0]
            self.Du_Mua = self.TCB_Data['Khối lượng Dư mua'].values[0]
            self.Du_Ban = self.TCB_Data['Khối lượng Dư bán'].values[0]
            self.Price_At_Max_Vol = self.TCB_Data['Khớp nhiều nhất'].values[0]
        except:
            self.TCB_valuation = 0
            self.max_price_year = 0
            self.min_price_year = 0
            self.MA20 = 0
            self.MA50 = 0
            self.MA100 = 0
            self.RSI = 0
            self.PB = 0
            self.PE = 0
            self.ROE = 0

            self.signal_KT = 0
            self.signal_TBD = 0
            self.MACD_Signal = 0
            self.MACD_Volume = 0
            self.Du_Mua = 0
            self.Du_Ban = 0
            self.Price_At_Max_Vol = 0
        self.intraday = AnalysisIntradayData(self.name)
    
    def Load_Daily_Data(self) -> pd.DataFrame:
        return db.GetStockData(self.name)

    @property
    def intraday_price(self):
        try:
            return self.TCB_Data['Giá Khớp Lệnh'].values[0]/1000
        except:
            return 0

    @property
    def price(self):
        if(self.intraday_price != self.prices[0]):
            return self.intraday_price
        else:
            return self.prices[0]

    @property
    def review_price(self):
        output = f'Giá'
        output += f'\n- MA20 {self.MA20:,.2f} : {percent(self.price,self.MA20):,.2f}(%)'
        output += f'\n- MA50 {self.MA50:,.2f} : {percent(self.price,self.MA50):,.2f}(%)'
        output += f'\n- MA100 {self.MA100:,.2f} : {percent(self.price,self.MA100):,.2f}(%)'
        output += f'\n'
        if(self.price >= self.MA100 and self.price >= self.MA50 and self.price >= self.MA20):
            output += f'- Vượt tất cả các mốc MA quan trọng\n'
        if(self.price >= self.max_price_year):
            output += f'- Vượt đỉnh năm: {percent(self.price,self.max_price_year):,.2f} (%)'
        elif(self.price <= self.min_price_year):
            output += f'- Thủng dáy năm: {percent(self.price,self.min_price_year):,.2f} (%)'
        else:
            output += f'- Chưa có gì đặc biệt'
        return output

    @property
    def review_volume(self):
        output = f'Khối lượng'
        output += f'\n- CN/TN: {self.max_vol:,.0f} | {self.min_vol:,.0f} | {self.avg_vol:,.0f}'
        output += f'\n- HT: {self.daily_volumes[0]:,.0f} : {percent(self.daily_volumes[0],self.avg_vol):,.2f}(%)'        
        return output
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
        output = f'- Định giá: {valuation:,.2f} | {percent(self.price,valuation):,.2f} (%)'
        if(self.price <= valuation):
            output += ' => Hấp dẫn'
        else:
            output += ' => Cao, xem lại'
        return output
        
    @property
    def signals(self):
        output = f'Tín hiệu (TA):'
        output + f'\n- Kỹ thuật: {self.signal_KT}'
        output += f'\n- Trung bình động: {self.signal_TBD}'
        output += f'\n- MACD: {self.MACD_Signal}'
        output += f'\n- MACD (Volume): {self.MACD_Volume}'
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

    def get_min_vols(self):
        results = []
        start = 0
        end = len(self.df_data)-20
        for i in range(start,end):
            if self.is_min_vol(i):                
                results.append(i)
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

    @property
    def liquidity(self):
        return self.daily_money[0]/billion #Tỷ
    @property
    def liquidity_max(self):
        return np.max(self.daily_money)/billion #Tỷ
    @property
    def liquidity_min(self):
        return np.min(self.daily_money)/billion #Tỷ

    def Describe(self):
        output = f'{self.name} - {self.price} | {self.last_pct_price:,.2f}(%)| {self.last_trans_date}'       
        output += f'\n{self.review_price}'
        output += f'\n{self.review_volume}'               
        output += f'\nThanh khoản: {self.liquidity:,.2f} (tỷ) | CN/TN: {self.liquidity_max:,.2f} | {self.liquidity_min:,.2f}'
        output += f'\n{self.review}'
        output += f'\n{self.signals}'        
        output += f'\n{"-"*30}'
        output += f'\n{self.intraday.GetSummary()}'
        d = DayData(symbol=s.name, index = 0,df_all_data=s.df_data,count_days=10)
        output += f'\n{d.summary}'
        return output

# stocks = ['VND']
# for s in stocks:
#     s = Stock(name=s)
#     #print(f'{s.name} - {s.rate_of_waze}')
    
#     #d = DayData(symbol=s.name, index = 0,df_all_data=s.df_data,count_days=10)
#     print(f'{s.Describe()}')

# stocks = ['KSB','TPB','VND','KBC','CEO','BID','CTG']
# for s in stocks:
#     s = Stock(name=s)
#     #s.check_pivots()
#     s.check_min_vol()

# import heapq
# stocks = ['CTG', 'BID','HAX','VND']
# for symbol in stocks:
#     s = Stock(name = symbol)
#     p = PriceAction(symbol=s.name,df_data=s.df_data,days=100)
#     print(f'{symbol} - {p.analysis_last_price}')
# top_10 = heapq.nlargest(n=10,iterable=p.prices)
# print(top_10)
# low_10 = heapq.nsmallest(n=10,iterable=p.prices)
# print(low_10)
