from DateHelper import *
from CandleStick import CandleStick

class DayData:
    def __init__(self, symbol, index, df_all_data, count_days) -> None:
        self.symbol = symbol.upper()        
        self.df_all_data = df_all_data
        self.df_data = self.df_all_data[self.index:self.index+self.T_days]        
        self.df_next_data = self.get_df_next_data()

        self.index = index
        self.T_days = count_days

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
        self.avg_oscillation_low = np.average(self.df_data['Oscillation-Low-Open'])
        self.avg_oscillation_high = np.average(self.df_data['Oscillation-Open-High'])

        self.CandleStick = CandleStick(open=self.open,close=self.close,high=self.high,low=self.low,volume=self.volume, index=0)

        self.singal = ''

    @property
    def today_money(self):
        return self.volume*self.price/billion #tỷ

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
        return np.max(self.df_data['Oscillation-Open-High'])
    
    @property
    def max_desc_oscillation_open(self):
        return np.min(self.df_data['Oscillation-Low-Open'])
    
    @property
    def target_buy_price(self):
        price = (self.avg_oscillation_low/100)*self.price + self.price
        return price

    @property
    def target_sell_price(self):        
        price = (self.avg_oscillation_high/100)*self.price + self.price
        return price
    
    @property
    def isFL(self):
        if self.margin_price <= -6.67:
            return True
        else:
            return False
    
    @property
    def isCE(self):
        if self.margin_price >= 6.67:
            return True
        else:
            return False

    @property
    def is_min_price(self):
        min = np.min(self.df_data['Close'][1:])
        if self.price <= min:
            return True
        else:
            return False
    
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
    

    # def get_max_profit(self, next_days):
    #     return np.max(self.df_next_data[next_days:]['Close'])        
    
    # def get_min_profit(self, next_days):
    #     return np.min(self.df_next_data[next_days:]['Close'])

    def is_over_max_price(self):
        if self.max_price > self.last_max_price:
            return True
        else:
            return False

    def is_under_min_price(self):
        if self.min_price < self.last_min_price:
            return True
        else:
            return False

    def get_df_next_data(self):        
        try:
            df_next_data = self.df_all_data[self.index-self.T_days:self.index]
            return df_next_data
        except:
            return None

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

    def get_index_of_min_price(self): #MinP = Min Price
        min_price = np.min(self.df_data['Close'])
        index_of_min = self.df_data.index[self.df_data['Close']==min_price][0]#.tolist()
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

    # def is_buy(self):
    #     _result = False
    #     if(self.is_max_vol() and self.margin_price<0):
    #         _result = True
    #     if(self.has_big_down_price() and self.has_big_up_price()):
    #         _result = True
    #     return _result

    # def get_signal(self):
    #     if (self.sum_margin_price <= -25):
    #         return True,'Chiết khấu sâu'
    #     else:
    #         return None,"Chưa xác định"
            
    # @property
    # def momentum(self):
    #     return self.get_distance_price()/self.T_days
    
    @property
    def summary(self):
        output = f'{self.symbol} - Phiên [{self.index}] - {self.close} [{self.margin_price:,.2f} (%)] - GTGD: {self.today_money:,.2f} (ỷ)'+\
        f'\nTrong {self.T_days} phiên : {self.sum_margin_price:,.2f}(%)'+\
        f'\n- Tăng {self.count_green} | Giảm {self.count_red} | Tham chiếu {self.count_yellow} : Tỷ lệ {self.count_green/self.count_red:,.2f}'+\
        f'\n- 03 phiên: {self.df_data["%"][0]:,.2f} | {self.df_data["%"][1]:,.2f} | {self.df_data["%"][2]:,.2f} | Tổng: {np.sum(self.df_data["%"][0:2]):,.2f} (%)'+\
        f'\n- Biến động CN: {np.max(self.df_data["Oscillation"]):,.2f} (%)'+\
        f'\n- Biến động TN {np.min(self.df_data["Oscillation"]):,.2f} (%)'+\
        f'\n- Biến động TB: {self.avg_oscillation:,.2f} (%)'+\
        f'\n- Biến động HT: {self.oscillation:,.2f} (%)'+\
        f'\nMax tăng/giảm: {self.max_inc_oscillation_open:,.2f} (%) | {self.max_desc_oscillation_open:,.2f} (%)'+\
        f'\nTB-Tăng: {np.average(self.avg_oscillation_high):,.2f} (%)| TB-Giảm: {self.avg_oscillation_low:,.2f} (%)'+\
        f'\nMục tiêu: \n- Mua {self.target_buy_price:,.2f} ({self.avg_oscillation_low:,.2f} (%))'+\
        f'\n- Bán: {self.target_sell_price:,.2f} ({self.avg_oscillation_high:,.2f}) (%)'+\
        f'\n=> Lợi nhuận: {percent(self.target_sell_price,self.target_buy_price):,.2f} (%)'+\
        f'\nGiá CN/TN: {self.max_price} | {self.min_price} [{self.get_index_of_min_price()}] [d = {self.get_distance_price():,.2f} (%)]'+\
        f'\nKLGD TB : {self.avg_vol:,.2f} - Min vol: {self.is_min_vol} - Max vol: {self.is_max_vol}, '+\
        f'\nMin price : {self.is_under_min_price()} , Max price: {self.is_over_max_price()}, '+\
        f'\nNN(Mua-Bán) {self.sum_foriegn:,.2f} ~ {(self.sum_foriegn/self.sum_vol)*100:,.2f} (%) - Min NN : {self.is_min_foriegn()}, - Max NN {self.is_max_foriegn()}'+\
        f'\n{"-"*30}\n'
        return output

    # def to_string(self):
    #     pass