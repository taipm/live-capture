from DayData import DayData
from Stock import Stock

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

    @property
    def has_supper_volume(self):
        if self.isEnoughVolume():
            if len(self.big_trends_up)>0:
                return True
        else:
            return False

    def _str_(self):
        ouput = f'{self.name} - {self.len} - {self.price} - {self.vol}'
        ouput += f'DayData: {len(self.days)} - First: {self.days[0]}'
        return ouput

    def summary(self):
        output = ''
        if self.has_supper_volume:
            output += f'\n{self.name}'
            for d in self.big_trends_up:
                output += f'\n{d.index} - {d.price} - {d.date}'
                output += f'\n{super().summary()}'
                output += f'\n{"-"*30}'
        return output