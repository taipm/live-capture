from Caculator import *
import numpy as np
from DateHelper import *
from Constant import *
import pandas as pd

class DateData:
    '''
    DỮ LIỆU HÀNG NGÀY
    '''
    def __init__(self, symbol, index, df_all_data) -> None:
        self.symbol = symbol.upper()
        self.index = index
        self.df_all_data = df_all_data
        self.data_item = self.df_all_data.iloc[index]
        
        self.date  = self.data_item['Date']
        self.close = self.data_item['Close']
        self.open = self.data_item['Open']
        self.high = self.data_item['High']
        self.low = self.data_item['Low']
        self.volume = self.data_item['Volume']
        self.margin = self.data_item['%']

        self.foriegn_buy = self.data_item['NN Mua']
        self.foriegn_sell = self.data_item['NN Ban']

    @property
    def price(self):
        if self.close > 0:
            return self.close
        else:
            return self.open

    @property
    def isFL(self):
        if self.margin <= -6.67:
            return True
        else:
            return False
    @property
    def isGreen(self):
        if self.close >= self.open and self.margin >= 1:
            return True
        else:
            return False
    @property
    def isCE(self):
        if self.margin >= 6.67:
            return True
        else:
            return False

    def analysis(self):
        pass

    def __str__(self) -> str:
        return f'{self.symbol} | {self.price:,.2f}'+\
            f'{self.volume:,.0f}'

class DayData: #NÊN SỬA LẠI TÊN CHO PHÙ HỢP VỚI KHÔNG GIAN COUNT_DAYS DỮ LIỆU
    def __init__(self, symbol, index, df_all_data, count_days) -> None:
        self.symbol = symbol.upper()
        self.index = index
        self.T_days = count_days

        self.df_all_data = df_all_data
        self.df_data = self.df_all_data[self.index:self.index + self.T_days]        
        self.df_next_data = self.get_df_next_data()

        self.data_item = self.df_all_data.iloc[index]
        self.date  = self.data_item['Date']
        self.close = self.data_item['Close']
        self.open = self.data_item['Open']
        self.high = self.data_item['High']
        self.low = self.data_item['Low']
        self.volume = self.data_item['Volume']

        self.foriegn_buy = self.data_item['NN Mua']
        self.foriegn_sell = self.data_item['NN Ban']
        
        self.sum_foriegn = np.sum(self.df_data['NN'])
        self.sum_margin_price = np.sum(self.df_data['%'])
        self.sum_vol = np.sum(self.df_data['Volume'])

        self.max_desc_price = np.min(self.df_data['%'])
        self.max_inc_price = np.max(self.df_data['%'])
        self.min_price = np.min(self.df_data['Close'])
        self.max_price = np.max(self.df_data['Close'])
        self.last_max_price = np.max(self.df_data['Close'][1:])
        self.last_min_price = np.min(self.df_data['Close'][1:])
        
        self.avg_vol = np.average(self.df_data['Volume'])
        self.min_vol = np.min(self.df_data['Volume'])
        self.max_vol = np.max(self.df_data['Volume'])
        self.last_max_vol = np.max(self.df_data['Volume'][1:])
        self.last_min_vol = np.min(self.df_data['Volume'][1:])

        self.avg_oscillation = np.average(self.df_data['Oscillation'])
        self.avg_oscillation_down = np.average(self.df_data['Oscillation-Down'])
        self.avg_oscillation_up = np.average(self.df_data['Oscillation-Up'])

        #self.dates_data = self.mapperToDateData()

        self.singal = ''

    # def mapperToDateData(self):
    #     dates_data = []
    #     for i in range(0,len(self.df_all_data)-1):            
    #         dateData = StockDateData(symbol=self.symbol,index=i, df_all_data=self.df_all_data)
    #         dates_data.append(dateData)
    #     return dates_data

    @property
    def today_money(self):
        return self.volume*self.price/billion

    @property
    def t0_profit(self):
        return profit(mua=self.low, ban=self.high)
    @property
    def max_profit(self):
        '''
        Lợi nhuận cao nhất trong T_days
        '''
        max_price = np.max(self.df_next_data['High'])
        return profit(mua=self.low,ban=max_price)
        
    @property
    def price(self):
        if self.close > 0:
            return self.close
        else:
            return self.open

    @property
    def count_red(self):
        return len(self.df_data[self.df_data['%']<0])
    
    @property
    def count_green(self):
        return len(self.df_data[self.df_data['%']>0])
    
    @property
    def count_yellow(self):
        return len(self.df_data[self.df_data['%']==0])
    
    @property
    def oscillation(self):
        return self.df_data['Oscillation'][self.index]
    
    @property
    def max_inc_oscillation_open(self):
        return np.max(self.df_data['Oscillation-Up'])
    
    @property
    def max_desc_oscillation_open(self):
        return np.min(self.df_data['Oscillation-Down'])
    
    def target_buy_price(self, desc_rate):
        '''
        Chỉ mua khi giảm quá -6% và nên bán trong phiên
        '''
        price = inc_percent(self.price,desc_rate)
        return price

    def target_sell_price(self, inc_rate):      
        price = inc_percent(self.target_buy_price(desc_rate=-6),inc_rate+0.67)
        return price
    
    @property
    def isFL(self):
        if self.margin_price <= -6.67:
            return True
        else:
            return False
    @property
    def isGreen(self):
        if self.close >= self.open and self.margin_price>=1:
            return True
        else:
            return False
    @property
    def isCE(self):
        if self.margin_price >= 6.67:
            return True
        else:
            return False

    '''
    VOLUME ANALYSIS
    '''
    def is_supper_volume(self,level):
        if self.volume >= level*self.last_max_vol and self.margin_price >=1:
            return True
        elif self.is_max_vol and self.isGreen:
            return True
        else:
            return False

    def is_break_volume(self,level):
        if self.volume >= level*self.avg_vol and self.margin_price >=2:
            if self.volume >= self.last_max_vol:
                if self.close > self.open:
                    return True
        else:
            return False
    
    def is_big_trend_up(self):
        level = 3
        result = False
        if self.volume >= level*self.avg_vol and self.margin_price >=3:
            if self.isGreen:
                result = True
        return result

    def is_big_trend_down(self):
        level = 5
        if self.volume >= level*self.last_max_vol and self.margin_price < 0:
            return True
        else:
            return False

    @property
    def pct_avg_volume(self):
        return percent(self.volume,self.avg_vol)

    @property
    def is_min_vol(self):
        if(self.volume <= self.last_min_vol):
            return True
        else:
            return False
    
    @property
    def is_max_vol(self):
        if(self.volume >= self.last_max_vol):
            return True
        else:
            return False
    @property
    def margin_price(self):
        return self.df_data['%'][self.index]
    
    @property
    def margin_volume(self):
        return percent(self.df_data['Volume'][self.index],self.df_data['Volume'][self.index+1])
    
    @property
    def review_volume(self):
        output = ''
        if(self.is_max_vol):
            output += f'{self.volume} - MaxVol {self.T_days} ngày'
        elif(self.is_min_vol):
            output += f'{self.volume} - MinVol {self.T_days} ngày'
        return output
    @property
    def review_price(self):
        output = f'Giá:\n'
        if(self.is_max_price):
            output += f'{self.max_price} - max: {self.T_days} ngày'
        elif(self.is_min_price):
            output += f'{self.min_price} - min {self.T_days} ngày'
        output += f'- Giá CN/TN: {self.max_price} | {self.min_price} [{self.get_index_of_min_price()}] [d = {self.get_distance_price():,.2f} (%)]'
        return output
    
    # def isMaxPrice(self):
    #     trail_prices = self.df_data[1:]
    #     if(self.price >= np.max(trail_prices)):
    #        return True
    #     else:
    #         return False

    @property
    def is_max_price(self):
        if(self.price >= self.last_max_price):
            return True
        else:
            return False
    @property
    def is_min_price(self):
        if(self.price <= self.last_min_price):
            return True
        else:
            return False
            
    @property
    def is_highest_price(self):
        if self.close == self.high:
            return True
        else:
            return False
    @property
    def is_lowest_price(self):
        if self.close == self.low:
            return True
        else:
            return False

    def get_df_next_data(self) -> pd.DataFrame:
        try:
            df_next_data = self.df_all_data[self.index-self.T_days:self.index+1]            
            return df_next_data.reset_index(drop=True)
        except:
            return pd.DataFrame().empty
   
    def isUpPrice(self,x:float): #Up x%
        if x > 0:
            if self.margin_price >= x:
                return True
            else:
                return False
        else:
            if self.margin_price < x:
                return True
            else:
                return False

    def isUpVolume(self,x:float): #Up 3%
        if self.margin_volume >= x:
            return True
        else:
            return False

    def is_min_foriegn(self):
        days_to_count = self.T_days
        min_foriegn = np.min(self.df_all_data[self.index:self.index + days_to_count]['NN'])
        if(self.close == min_foriegn):
            return True
        else:
            return False

    def is_max_foriegn(self):
        days_to_count = self.T_days
        max_foriegn = np.max(self.df_all_data[self.index:self.index + days_to_count]['NN'])
        if(self.close == max_foriegn):
            return True
        else:
            return False
    
    def get_distance_price(self):
        min = self.min_price
        max = self.max_price
        distance = ((max-min)/min)*100
        return distance

    def get_index_of_min_price(self):
        min_price = np.min(self.df_data['Close'])
        index_of_min = self.df_data.index[self.df_data['Close']==min_price][0]
        return index_of_min
    
    def get_max_profit(self):
        min_price = self.min_price
        index_of_min = self.get_index_of_min_price()
        max_from_min_index = np.max(self.df_data['Close'][0:index_of_min])
        profit = percent(min_price,max_from_min_index)
        return profit
    
    def get_max_desc_price(self):
        return np.min(self.df_data['%'])
    
    def get_max_inc_price(self):
        return np.max(self.df_data['%'])

    def has_big_down_price(self):
        if(self.get_max_desc_price() <= -5):
            return True
        return False
    
    def has_big_up_price(self):
        if(self.get_max_inc_price() >= 5):
            return True
        return False

    def update_signal(self, text):
        return self.singal + '\n' + text
    
    @property
    def review_foriegn(self):
        output = ''
        output += f'NN(Mua-Bán) {self.sum_foriegn:,.2f} ~ {(self.sum_foriegn/self.sum_vol)*100:,.2f} (%) - Min NN : {self.is_min_foriegn()}, - Max NN {self.is_max_foriegn()}'
        return output

    @property
    def summary(self):
        output = f'{self.symbol} - Phiên [{self.index}] - {self.close} [{self.margin_price:,.2f} (%)] - GTGD: {self.today_money:,.2f} (tỷ)'+\
        f'\nTrong {self.T_days} phiên : {self.sum_margin_price:,.2f}(%)'+\
        f'\n- Tăng {self.count_green} | Giảm {self.count_red} | Tham chiếu {self.count_yellow} : Tỷ lệ {self.count_green/self.count_red:,.2f}'+\
        f'\n- 03 phiên: {self.df_data["%"][0]:,.2f} | {self.df_data["%"][1]:,.2f} | {self.df_data["%"][2]:,.2f} | Tổng: {np.sum(self.df_data["%"][0:2]):,.2f} (%)'+\
        f'\n- Biến động CN/TN: {np.max(self.df_data["Oscillation"]):,.2f} (%) | {np.min(self.df_data["Oscillation"]):,.2f} (%)'+\
        f'\n- Biến động TB: {self.avg_oscillation:,.2f} (%)'+\
        f'\n- Biến động HT: {self.oscillation:,.2f} (%)'+\
        f'\nMax tăng/giảm: {self.max_inc_oscillation_open:,.2f} (%) | {self.max_desc_oscillation_open:,.2f} (%)'+\
        f'\nTB-Tăng: {np.average(self.avg_oscillation_up):,.2f} (%)| TB-Giảm: {self.avg_oscillation_down:,.2f} (%)'+\
        f'\nMục tiêu: \n- Mua {self.target_buy_price(desc_rate=-6):,.2f} -6(%)'+\
        f'\n- Bán:'+\
        f'\n- 3%: {self.target_sell_price(3):,.2f} | 4%: {self.target_sell_price(4):,.2f} | 5%: {self.target_sell_price(5):,.2f}'+\
        f'\n{self.review_price}'+\
        f'\nKLGD TB: {self.avg_vol:,.2f}: {self.pct_avg_volume:,.2f} (%) - {self.review_volume}'+\
        f'\nKhối ngoại:\n {self.review_foriegn}'+\
        f'\n{"-"*30}\n'
        return output