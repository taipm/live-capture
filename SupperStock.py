from DateHelper import StrTODAY
from DayData import DayData
from Stock import Stock
class SupperStock(Stock):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.dayObjs = self.scan()
    
    def scan(self):
        items = []
        for i in range(0,self.len-1):
            dayObj = DayData(symbol=self.name,index=i,df_all_data=self.df_data,count_days=10)
            items.append(dayObj)
        return items

    def get_supper_volumes(self):
        days = []
        for i in range(0, len(self.dayObjs)-1):
            if self.dayObjs[i].is_supper_volume(3):
                days.append(self.dayObjs[i])
            if self.dayObjs[i].is_supper_volume(2):
                days.append(self.dayObjs[i])
        return sorted(list(set(days)),key = lambda x : x.index)

    def get_break_volumes(self): #compare with avg_vol
        days = []
        for i in range(0, len(self.dayObjs)-1):
            if self.dayObjs[i].is_break_volume(2):
                days.append(self.dayObjs[i])
            # if self.dayObjs[i].is_supper_volume(2):
            #     days.append(self.dayObjs[i])
        return sorted(list(set(days)),key = lambda x : x.index)

    @property
    def has_supper_volume(self):
        if len(self.get_supper_volumes())>0:
            return True
        else:
            return False
    @property
    def has_break_volume(self):
        if len(self.get_break_volumes())>0:
            return True
        else:
            return False

    def to_string(self):
        df_data = self.df_data
        ouput = f'{self.name} - {self.len} - {self.price} - {self.vol}'
        ouput += f'DayData: {len(self.dayObjs)} - First: {self.dayObjs[0]}'
        return ouput


# from db import *
# #stocks = list(set(['HAX','DGW', 'FRT','DIG','CEO','PVT']))

# stocks = get_danhmuc_symbols()
# rs = []
# for s in stocks:
#     try:
#         s = SupperStock(name=s)
#         #print(txt)
#         print(f'{s.name} - Break vol: {s.has_break_volume}')
#         if s.has_break_volume:
#             points = s.get_break_volumes()
#             for p in points:
#                 if(p.index <= 30):
#                     rs.append([p.symbol, p.index, p.price, p.volume, p.date])
#                     print(f'{p.index} - {p.price} - {p.volume} {p.date}')
#         print(f'{"-"*20}')
#     except:
#         continue
# df = pd.DataFrame(rs,columns=['symbol','index','price','volume','date'])
# df.to_excel(f'./data/{StrTODAY}-pivots.xlsx')
# stocks = get_banks_symbols()
# for s in stocks:
#     s = SupperStock(name=s)
#     #print(txt)
#     print(f'{s.name} - Khủng long thức giấc: {s.has_supper_volume}')
#     if s.has_supper_volume:
#         points = s.get_supper_volumes()
#         for p in points:
#             #if(p.index <= 30):
#             print(f'{p.index} - {p.price} - {p.volume} {p.date}')
#     print(f'{"-"*20}')