from DateHelper import *

class DayData:
    def __init__(self, symbol, index, df_all_data) -> None:
        self.symbol = symbol.upper()        
        self.df_all_data = df_all_data
        self.index = index
        self.data_item = self.df_all_data.iloc[index]
        self.date  = self.data_item['Date']
        self.close = self.data_item['Close']
        self.open = self.data_item['Open']
        self.high = self.data_item['High']
        self.low = self.data_item['Low']
        self.volume = self.data_item['Volume']
        self.foriegn_buy = self.data_item['NN Mua']
        self.foriegn_sell = self.data_item['NN Ban']
        self.T_days = 10
        self.df_data = self.df_all_data[self.index:self.index+self.T_days]

    def is_min_vol(self):
        days_to_count = self.T_days
        min_vol = np.min(self.df_all_data[self.index:self.index + days_to_count]['Volume'])
        if(self.volume == min_vol):
            return True
        else:
            return False
    
    def is_max_vol(self):
        days_to_count = self.T_days
        max_vol = np.max(self.df_all_data[self.index:self.index + days_to_count]['Volume'])
        if(self.volume == max_vol):
            return True
        else:
            return False

    def is_min_price(self):
        days_to_count = self.T_days
        min_price = np.min(self.df_all_data[self.index:self.index + days_to_count]['Close'])
        if(self.close == min_price):
            return True
        else:
            return False

    def is_max_price(self):
        days_to_count = self.T_days
        max_price = np.max(self.df_all_data[self.index:self.index + days_to_count]['Close'])
        if(self.close == max_price):
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

    def get_margin_price(self):
        days_to_count = self.T_days
        df_margin_p = ((self.df_all_data['Close']-self.df_all_data['Open'])/self.df_all_data['Open'])*100
        percent_price = np.sum(df_margin_p[self.index:self.index+days_to_count])
        return percent_price

    def get_min_price(self):
        min_price = np.min(self.df_data['Close'])
        return min_price

    def get_max_price(self):
        max_price = np.max(self.df_data['Close'])
        return max_price
    
    def get_distance_price(self):
        min = self.get_min_price()
        max = self.get_max_price()
        distance = ((max-min)/min)*100
        return distance

    def get_index_of_min_price(self): #MinP = Min Price
        min_price = np.min(self.df_data['Close'])
        index_of_min = self.df_data.index[self.df_data['Close']==min_price][0]#.tolist()
        return index_of_min
    
    def get_max_profit(self):
        min_price = self.get_min_price()
        index_of_min = self.get_index_of_min_price()
        max_from_min_index = np.max(self.df_data['Close'][0:index_of_min])
        profit = percent(min_price,max_from_min_index)
        return profit
    # def get_speed_of_price(self):
    #     range_price = 
    #def is_buy(self):

    def to_string(self):
        #print(self.data_item)
        #åprint(f'{self.date} - {self.open}, {self.close} , {self.high}')

        print(  f'{self.symbol} - Phiên [{self.index}] - {self.close} - Trong {self.T_days} phiên : {self.get_margin_price():,.2f}(%)'
                f'\nGiá CN/TN: {self.get_max_price()} | {self.get_min_price()} [d = {self.get_distance_price():,.2f} (%)'
                f'\nLN cao nhất: {self.get_max_profit():,.2f} (%)'
                f'\nGiá TN: {self.get_min_price()} tại phiên {self.get_index_of_min_price()}'
                f'\nMin vol: {self.is_min_vol()} - Max vol: {self.is_max_vol()}, '
                f'\nMin price : {self.is_min_price()} , Max price: {self.is_max_price()}, '
                f'\nMin NN : {self.is_min_foriegn()}, - Max NN {self.is_max_foriegn()}'
        )

# s = Stock(name = 'VND')
# s.Prepare()
# d = DayData(symbol='VND',index=0,df_all_data=s.df_data)
# d.to_string()

class DateStick:
    def __init__(self, symbol, date, close, high, low, open, volume, foriegn_buy, foriegn_sell, df_all_data) -> None:
        self.symbol = symbol.upper()
        self.df_all_data = df_all_data
        self.date  = date
        self.close = close
        self.open = open
        self.high = high
        self.low = low
        self.volume = volume
        self.foriegn_buy = foriegn_buy
        self.foriegn_sell = foriegn_sell
    
    def to_string(self):
        print(f'CP: {self.symbol} - Date {self.date} : Close: {self.close} Open: {self.open} High: {self.high}')
    

    # def is_up(self) -> bool:
    #     if (self.close == self.high):
    #         return True
    
    # def is_down(self) -> bool:
    #     if(self.close == self.low):
    #         return True

    # def forecast(self):
    #     if self.is_up():
    #         return 'UP'
    #     elif self.is_down():
    #         return 'DOWN'
    #     else:
    #         return None     

    # def get_next_day_stick(self):
    #     next_date = self.date - timedelta(days = 1)
        
    #def check_forcast(self):

