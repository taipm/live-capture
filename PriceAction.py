import numpy as np
from Caculator import percent

class PriceRanges:
    def __init__(self, min, max, high) -> None:
        self.min = min
        self.max = max
        self.high = high
        self.ranges = self.get_ranges()        

    def get_ranges(self):
        start = self.min
        end = self.max
        ranges = []

        low = start
        top = start + start*self.high
        while top <= end:
            ranges.append([low,top])
            low = top
            top = top + top*self.high
        return ranges

    def indexOf(self, number):
        index = -1
        for i in range(0, len(self.ranges)-1):
            r = self.ranges[i]
            # print(f'{r[0]} - {r[1]}')
            if r[0] < number and r[1] >= number:
                index = i
                #print(f'Đoạn này: {r[0]} - {r[1]}')
                break
            # i = i + 1
                
        return index

# r = PriceRanges(min=1,max=10,high=10/100)
# r.get_ranges()
# print(r.indexOf(6))

class PriceRange:
    def __init__(self, min, max, length) -> None:
        self.min_price = min
        self.max_price = max
        self.length = length
        self.high = 5/100 #Default

    def nextRange(self):
        min = self.min_price + self.min_price*self.high
        max = self.max_price + self.max_price*self.high
        r = PriceRange(min= min,max=max,length=self.length)
        return r

    def isIn(self, number):
        if (number < self.min_price or number > self.max_price):
            return False
        else:
            return True
    def isOut(self,number):
        return not self.isIn(number=number)

    def isHigher(self,number):
        if (number > self.max_price):
            return True
        else:
            return False
    def isLower(self,number):
        if (number < self.max_price):
            return True
        else:
            return False    
                    
    def to_string(self):
        print(f'{self.max_price}')

# r = PriceRange(1,2,10)
# print(r.isIn(10))
# print(r.isOut(1.1))
# print(r.isOut(2.1))
# print(r.nextRange().to_string())
    
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
        self.days = len(self.prices)        
        self.start = self.prices[len(self.prices)-1]
        self.end = self.prices[0]
        self.ranges = PriceRanges(min=self.min_price, max= self.max_price,high=5/100)        
        self.index_price = self.ranges.indexOf(number = self.price)
    
    def print_ranges(self):
        for r in self.ranges.ranges:
            print(f'{r[0]} - {r[1]}')

    def get_indexs_by_price(self, price):
        results_found = self.df_data[self.df_data['Close']==price].index
        return results_found
    
    @property
    def suc_bat(self):
        df_strong = self.df_data[self.df_data['%']>=3]
        suc_bat = np.sum(df_strong['%'])/self.days
        return suc_bat
    @property
    def suc_bat_am(self):
        df_strong = self.df_data[self.df_data['%']<=-2.5]
        suc_bat = np.sum(df_strong['%'])/self.days
        return suc_bat
    @property
    def suc_manh(self):
        return self.suc_bat+self.suc_bat_am
        
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
    
    def isMaxPrice(self) -> bool:
        if(self.price > self.last_max_price):
           return True
        else:
            return False

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
        output += f'Giá HT: {self.price} | Giá TB: {self.avg_price:,.2f} : {percent(self.price,self.avg_price):,.2f} (%)'
        output += f'\nVùng giá thứ {self.index_price}'
        if(self.price < self.avg_price):
            output += ' : Dưới giá trung bình'
        else:
            output += ' : Trên giá trung bình'
        if(self.price <= np.min(trail_prices)):
            output += f'\n- Giá thấp nhất {self.days} ngày'
        elif(self.price > np.max(trail_prices)):
            output += f'\n- Vượt đỉnh {self.days} ngày'
        elif(self.price == np.max(trail_prices)):
            output += f'\n- Chạm đỉnh {self.days} ngày'        
        if(self.price_is_max and self.df_data['%'][0] >=3):
            output += f'\n=> Lưu ý: [TĂNG] mạnh khỏi nền giá'
        elif(self.price_is_min and self.df_data['%'][0] <=-3):
            output += f'\n=> Lưu ý: [RỚT] mạnh khỏi nền giá'
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