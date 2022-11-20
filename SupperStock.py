from BlogManager import Blog
from DateHelper import StrTODAY
from DayData import DayData
from Stock import Stock
from db import *
class SupperStock(Stock):
    def __init__(self, name) -> None:
        super().__init__(name)
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
                days.append(self.days[i])
        return sorted(list(set(days)),key = lambda x : x.index)

    @property
    def has_supper_volume(self):
        if len(self.big_trends_up)>0:
            return True
        else:
            return False

    def to_string(self):
        ouput = f'{self.name} - {self.len} - {self.price} - {self.vol}'
        ouput += f'DayData: {len(self.days)} - First: {self.days[0]}'
        return ouput

    def summary(self):
        output = ''
        if self.has_supper_volume:
            output += f'\n{self.name}'
            for d in self.big_trends_up:
                output += f'\n{d.index} - {d.price} - {d.date}'
        return output


class DailyReport:
    def __init__(self) -> None:
        self.title = f'{StrTODAY} - [Dấu hiệu] - Big trend UP'
        self.content = self.get_daily_report()

    def get_daily_report(self):
        output = ''
        stocks = get_danhmuc_symbols()
        stocks = ['DGC']
        for symbol in stocks:
            s = SupperStock(name=symbol)
            if (s.has_supper_volume):
                output += f'{s.summary()}'
        return output

    def updateBlog(self):
        title = self.title
        content = self.content
        blog = Blog()
        url = blog.post(title=title,content=content,tags='daily report')
        return url
        # post = BlogPost()
        # post.update_to_blog()
    
    def __str__(self) -> str:
        return f'{self.title}\n{self.content}'

d = DailyReport()
print(d)
#print(d.updateBlog())
# print(d.title)
# print(d.content)

# 
# stocks = list(set(['HAX','DGW', 'FRT']))

# for s in stocks:
#     s = SupperStock(name=s)
#     if (s.has_supper_volume):
#         print(f'{s} - {s.summary()}')

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