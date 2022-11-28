from DayData import DayData
from Stock import Stock
from StockNews import StockNews
from StockOwners import StockOwners

class SupperStock(Stock):
    def __init__(self, name) -> None:
        super().__init__(name)
        print(f'SupperStock: {self.name}')
        self.days = self.scan()
    
    def scan(self):
        items = []
        for i in range(0,self.len-1):
            day = DayData(symbol=self.name,index=i,df_all_data=self.df_data,count_days=10)
            items.append(day)
        return items

    @property
    def big_trends_up(self):
        days = []
        for i in range(0, len(self.days)-1):
            if self.days[i].is_big_trend_up():
                if (i <= 10):
                    days.append(self.days[i])
        return sorted(list(set(days)),key = lambda x : x.index)

    def isEnoughVolume(self):
        if (self.liquidity <= 5):
            return False
        else:
            return True

    def isMaxPrice(self)->bool:
        return self.priceAction.isMaxPrice()

    @property
    def has_supper_volume(self):
        result = False
        if self.isEnoughVolume():
            if len(self.big_trends_up)>0:
                result = True
        return result

    def _str_(self):
        ouput = f'{self.name} - {self.len} - {self.price} - {self.vol}'
        ouput += f'DayData: {len(self.days)} - First: {self.days[0]}'
        return ouput

    def summary(self):
        output = ''
        if self.has_supper_volume:
            output += f'\n{self.name}'
            owners = StockOwners(self.name)
            output += f'\n{owners.analysis()}'
            for d in self.big_trends_up:
                output += f'\n{d.index} - {d.price} - {d.date}'
                output += f'\n{super().summary()}'
                output += f'\n{"-"*30}'
        return output
    
    def summaryToBlog(self):
        output = ''
        if self.has_supper_volume:
            output += f'\n{self.name}'
            owners = StockOwners(self.name)
            news = StockNews(self.name)
            output += f'\n{owners.summaryToBlog()}'
            for d in self.big_trends_up:
                output += f'\n{d.index} - {d.price} - {d.date}'
                output += f'\n{super().summaryToBlog()}'
                output += f'\n{"-"*30}'
            output += f'\nTin tức: {news}'
        # elif self.isMaxPrice():
        #     output += f'\n{self.name}'
        #     owners = StockOwners(self.name)
        #     news = StockNews(self.name)
        #     output += f'\n{owners.summaryToBlog()}'
        #     output += f'\n{super().summaryToBlog()}'
        #     output += f'\n{"-"*30}'
        #     output += f'\nTin tức: {news}'
        return output