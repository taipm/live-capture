from Caculator import *
from DateData import DateData
from DayData import *
from DividendStock import DividendStock
from IntradayData import *
from StockOwners import StockOwners
from vnstocklib.StockChart import StockChart
import db
import pandas as pd
import numpy as np
from vnstock import *
    
class Stock:
    def __init__(self, name) -> None:
        self.name = name.upper()
        print(f'Stock: {self.name}')
        self.chartUrl = StockChart(symbol=self.name)
        self.df_data = self.Load_Daily_Data()
        self.IsOK = True
        if not self.df_data.empty:
            self.len = len(self.df_data.index)
            self.prices = self.df_data['Close']
            self.volumes = self.df_data['Volume']        
            self.daily_foreign = self.df_data['NN']
            self.daily_money = self.df_data['Money']
            self.daily_low_prices = self.df_data['Low']
            self.daily_high_prices = self.df_data['High']
            self.daily_open_prices = self.df_data['Open']
            self.daily_close_prices = self.df_data['Close']

            self.max_price = np.max(self.prices)
            self.min_price = np.min(self.prices)
            self.vol = self.volumes[0]
            self.max_vol = np.max(self.volumes)
            self.min_vol = np.min(self.volumes)
            self.avg_vol = np.average(self.volumes)
            
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
            self.intraday_price = 0
                
            #self.TODAY = DateData(symbol=self.name,index=0, df_all_data=self.df_data)
            self.TODAY = DateData(symbol=self.name,index=0, df_all_data=self.df_data)
        else:
            self.IsOK = False
        #self.intraday = AnalysisIntradayData(self.name)

        #self.load_TCB_data()
    
    def Load_Daily_Data(self) -> pd.DataFrame:
        return db.GetStockData(self.name)
    
    def load_TCB_data(self):
        data = price_board(self.name)
        print(data)
        if not data.empty:
            self.intraday_price = data['Gi?? Kh???p L???nh'].values[0]/1000
            self.TCB_valuation = data['TCBS ?????nh gi??'].values[0]/1000
            self.max_price_year = data['?????nh 1Y'].values[0]/1000
            self.min_price_year = data['????y 1Y'].values[0]/1000
            self.MA20 = data['MA20'].values[0]/1000
            self.MA50 = data['MA50'].values[0]/1000
            self.MA100 = data['MA100'].values[0]/1000
            self.RSI = data['RSI'].values[0]
            self.PB = data['P/B'].values[0]
            self.PE = data['P/E'].values[0]
            self.ROE = data['ROE'].values[0]*100

            self.signal_KT = data['T??n hi???u KT'].values[0]
            self.signal_TBD = data['T??n hi???u TB ?????ng'].values[0]
            self.MACD_Signal = data['MACD Signal'].values[0]
            self.MACD_Volume = data['MACD Volume'].values[0]
            self.Du_Mua = data['Kh???i l?????ng D?? mua'].values[0]
            self.Du_Ban = data['Kh???i l?????ng D?? b??n'].values[0]
            self.Price_At_Max_Vol = data['Kh???p nhi???u nh???t'].values[0] 
    
    @property
    def price(self):
        if(self.intraday_price != self.prices[0] and self.intraday_price != 0):
            return self.intraday_price
        else:
            return self.prices[0]

    @property
    def last_trans_date(self):
        return self.df_data['Date'][0]

    @property
    def liquidity(self):
        return self.daily_money[0]/billion #T???
    @property
    def liquidity_max(self):
        return np.max(self.daily_money)/billion #T???
    @property
    def liquidity_min(self):
        return np.min(self.daily_money)/billion #T???
    @property
    def liquidity_avg(self):
        return np.average(self.daily_money)/billion #T???

    @property
    def review_price(self):
        output = f'Gi??'
        output += f'\n- MA20 {self.MA20:,.2f} : {percent(self.price,self.MA20):,.2f}(%)'
        output += f'\n- MA50 {self.MA50:,.2f} : {percent(self.price,self.MA50):,.2f}(%)'
        output += f'\n- MA100 {self.MA100:,.2f} : {percent(self.price,self.MA100):,.2f}(%)'
        output += f'\n'
        if(self.price >= self.MA100 and self.price >= self.MA50 and self.price >= self.MA20):
            output += f'- V?????t t???t c??? c??c m???c MA quan tr???ng\n'
        if(self.price >= self.max_price_year):
            output += f'- V?????t ?????nh n??m: {percent(self.price,self.max_price_year):,.2f} (%)'
        elif(self.price <= self.min_price_year):
            output += f'- Th???ng d??y n??m: {percent(self.price,self.min_price_year):,.2f} (%)'
        else:
            output += f'- Ch??a c?? g?? ?????c bi???t'
        return output 
    @property
    def review_volume(self):
        output = f'Kh???i l?????ng'
        output += f'\n- CN/TN: {self.max_vol:,.0f} | {self.min_vol:,.0f} | {self.avg_vol:,.0f}'
        output += f'\n- HT: {self.volumes[0]:,.0f} : {percent(self.volumes[0],self.avg_vol):,.2f}(%)'        
        return output
    @property
    def review_ROE(self):
        output = f'ROE = {self.ROE:,.2f}'
        if self.ROE <= 10:
            output += f': Qu?? th???p'
        elif self.ROE >= 15 and self.ROE < 20:
            output += f': H???p l??'
        elif self.ROE >= 20:
            output += f': H???p d???n'
        return output
    @property
    def review_PB(self):
        output = f'PB = {self.PB:,.2f}'
        if self.PB <= 1:
            output += f': H???p d???n'
        elif self.PB >= 2 and self.PB < 3:
            output += f': H???p l??'
        elif self.PB >= 3:
            output += f': Qu?? cao'
        return output
    @property
    def review_RSI(self):
        output = f'RSI = {self.RSI:,.2f}'
        if self.RSI <= 30:
            output += f': Qu?? b??n'
        if self.RSI <= 35 and self.RSI > 30:
            output += f': G???n qu?? b??n'
        elif self.RSI >= 90:
            output += f': Qu?? mua'
        elif self.RSI >= 70 and self.RSI <= 85:
            output += f': ??ang n??ng ?????ng'
        return output
    @property
    def review_TCB_valuation(self):
        valuation = self.TCB_valuation
        output = f'?????nh gi??: {valuation:,.2f} | {percent(self.price,valuation):,.2f} (%)'
        if(self.price <= valuation):
            output += ' => H???p d???n'
        else:
            output += ' => Cao, xem l???i'
        return output
    
    def getDividend(self):
        return DividendStock(self.name).get_avg_dividend()
    @property
    def review_TA(self):
        output = f'T??n hi???u (TA):'
        output + f'\n- K??? thu???t: {self.signal_KT}'
        output += f'\n- Trung b??nh ?????ng: {self.signal_TBD}'
        output += f'\n- MACD: {self.MACD_Signal}'
        output += f'\n- MACD (Volume): {self.MACD_Volume}'
        return output
    @property
    def review(self):
        output = f'Nh???n x??t (c?? b???n) :'+\
            f'\n- {self.review_ROE}' +\
            f'\n- {self.review_RSI}' +\
            f'\n- {self.review_PB}' +\
            f'\n- {self.review_TCB_valuation}'
        return output

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

    def get_profit_by_index(self,index, pre_count_of_days):
        price = self.df_data.iloc[index]['Close']
        n_price = self.df_data.iloc[index-pre_count_of_days]['Close']
        return percent(price,n_price)

    def getIndex(self, str_date:str):
        data_item = self.df_data[self.df_data['Date'].map(lambda d:str(d)==str_date)]
        #print(data_item)
        return data_item
    # def getProfit(self, fromDate:datetime, toDate:datetime):
    #     from_index = self.(fromDate)

    def summary(self):
        output = f'{self.name} - {self.price} | {self.df_data["%"][0]:,.2f}(%)| {self.last_trans_date}'                
        output += f'\nThanh kho???n: {self.liquidity:,.2f} (t???) | CN/TN: {self.liquidity_max:,.2f} | {self.liquidity_min:,.2f}'
        output += f'\n{self.review}'
        output += f'\n{self.review_TA}'        
        output += f'\n{"-"*30}'
        
        if not self.intraday.hasError:
            output += f'\n{self.intraday.summary()}'

        d = DayData(symbol=self.name, index = 0,df_all_data=self.df_data,count_days=10)
        output += f'\n{d.summary}'

        f = DividendStock(symbol=self.name)
        output += '\nC??? t???c: ' + f.get_avg_dividend()
        
        #output += Buyer(self.name).summary()

        output += f'\n{self.chartUrl.imageUrl}'
        output += f'\n{self.chartUrl.dailyChartUrl}'
        output += f'\n{self.chartUrl.weeklyChartUrl}'
        return output
    
    def summaryToBlog(self):
        #self.priceAction = PriceAction(symbol=self.name,df_data=self.df_data,days=10)
        self.intraday = AnalysisIntradayData(self.name)
        self.load_TCB_data()

        output = f'{self.name} - {self.price} | {self.df_data["%"][0]:,.2f}(%)| {self.last_trans_date}'              
        output += f'\nThanh kho???n: {self.liquidity:,.2f} (t???) | CN/TN: {self.liquidity_max:,.2f} | {self.liquidity_min:,.2f}'
        output += f'\n{self.review}'
        output += f'\n{self.review_TA}'        
        output += f'\n{"-"*30}'
        if not self.intraday.hasError:
            output += f'\n{self.intraday.summary()}'

        d = DayData(symbol=self.name, index = 0,df_all_data=self.df_data,count_days=10)
        output += f'\n{d.summary}'

        f = DividendStock(symbol=self.name)
        output += f'\nC??? t???c: ' + f.get_avg_dividend()
        o = StockOwners(symbol=self.name)
        output += f'\nC??? ????ng l???n: {o.summaryToBlog()} '
        
        #output += Buyer(self.name).summary()
        output += f'\n{self.chartUrl.dailyChartUrl}'
        output += f'\n{self.chartUrl.weeklyChartUrl}'
        return output
