import numpy as np
from DateHelper import percent
from MessageHelper import border_text

class PriceItem:
    def __init__(self, high,low,open, close, index) -> None:
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.index = index

    def to_string(self):
        return f'{self.index} : {self.price:,.2f}'

class PriceAction:
    def __init__(self, symbol, df_data, days) -> None:
        self.symbol = symbol.upper()

        self.df_data = df_data[0:days]
        self.prices = self.df_data['Close']

        self.price = self.prices[0]
        self.min_price = np.min(self.prices)
        self.max_price = np.max(self.prices)
        self.last_max_price = np.max(self.prices[1:])
        self.last_min_price = np.min(self.prices[1:])
        self.avg_price = np.average(self.prices)

        #self.high = self.max_price - self.min_price
        self.days = len(self.prices)
        #self.speed = self.high/self.days
        self.start = self.prices[len(self.prices)-1]
        self.end = self.prices[0]
        #self.first = PriceItem(price = self.prices[0], index=0)
    
    def get_indexs_by_price(self, price):
        results_found = self.df_data[self.df_data['Close']==price].index
        return results_found

    @property
    def count_inc(self):
        count = len(self.df_data[self.df_data['%']>0])
        return count

    @property
    def count_desc(self):
        count = len(self.df_data[self.df_data['%']<0])
        return count

    @property
    def count_equal(self):
        count = len(self.df_data[self.df_data['%']==0])
        return count

    @property
    def count_over_avg(self):
        count = len(self.df_data[self.df_data['Close']>=self.avg_price])
        return count

    @property
    def max_inc(self):
        return np.max(self.df_data['%'])
    
    @property
    def max_desc(self):
        return np.min(self.df_data['%'])
    
    @property
    def price_is_max(self):
        trail_prices = self.prices[1:]
        if(self.price >= np.max(trail_prices)):
           return True
        else:
            return False
    @property
    def price_is_min(self):
        trail_prices = self.prices[1:]
        if(self.price <= np.min(trail_prices)):
           return True
        else:
            return False
    @property
    def min_index(self):
        return self.get_indexs_by_price(self.min_price).values[0]
    @property
    def max_index(self):
        return self.get_indexs_by_price(self.max_price).values[0]
    @property
    def analysis_last_price(self):
        trail_prices = self.prices[1:]
        output = ''
        output += f'Giá HT: {self.price} | Giá TB: {self.avg_price:,.2f}'
        if(self.price < self.avg_price):
            output += ' : Dưới giá trung bình'
        else:
            output += ' : Trên giá trung bình'
        if(self.price <= np.min(trail_prices)):
            output += f'Giá thấp nhất {self.days} ngày'
        elif(self.price > np.max(trail_prices)):
            output += f'Vượt đỉnh {self.days} ngày'
        elif(self.price == np.max(trail_prices)):
            output += f'Chạm đỉnh {self.days} ngày'
        
        if(self.price_is_max and self.df_data['%'][0] >=3):
            output += border_text(f'=> Lưu ý: [TĂNG] mạnh khỏi nền giá')
        elif(self.price_is_min and self.df_data['%'][0] <=-3):
            output += border_text(f'=> Lưu ý: [RỚT] mạnh khỏi nền giá')
        return output
    
    def actions(self, days):
        output = ''
        begin = 0
        end = days
        output += f'Diễn biến {days} phiên: {np.sum(self.df_data["%"][begin:end]):,.2F} (%)\n'
        for i in range(begin,end):
            output += f'{self.df_data["%"][end-i-1]} (%) | '
        output = output[0:len(output)-2]
        return output

    @property
    def summary(self):
        output = f'Hành động giá {self.days} phiên: {self.symbol}'+\
            f'\n{self.analysis_last_price}'+\
            f'\nTăng/giảm mạnh nhất: {self.max_inc} (%) : {self.max_desc} (%)'+\
            f'\n{self.actions(days = 5)}' +\
            f'\nGiá TN/CN/TB: {self.min_price} [{self.min_index}] : {self.max_price} [{self.max_index}]| {self.avg_price:,.2f}'+\
            f'\nTăng {self.count_inc} | Giảm {self.count_desc} | TC {self.count_equal}'+\
            f'\nKhung giá : {self.rectangle_price[0]:,.2f}'+\
            f'\nTỷ lệ >= AVG: {self.count_over_avg/self.days:,.2f} (%)'
        if(self.is_slight()):
            output += '\nNền giá : NGANG - Siết chặt'
        return output

    @property
    def rectangle_price(self):
        tall = percent(self.last_max_price,self.last_min_price)
        long = self.days-1
        return tall,long

    def is_slight(self):
        limit_tall = 10
        tall = self.rectangle_price[0]
        if tall <= limit_tall:
            return True
        else:
            return False

# import Stock
# s = Stock.Stock(name = 'HAG')
# s.Prepare()

# p = PriceAction(symbol=s.name,df_data=s.df_data,days=10)
# print(p.summary)
