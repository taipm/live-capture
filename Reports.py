from BlogManager import Blog
from PriceAction import PriceAction
from Stock import *
from SupperStock import SupperStock
from db import *
import pandas as pd

def get_stocks_by_suc_manh(command):
    command = command.upper()
    stocks = []
    if(command == 'BANKS'):
        stocks = db.get_banks_symbols()
    elif(command == 'CK'):
        stocks = db.get_securities_symbols()
    elif(command == 'DM'):
        stocks = db.get_danhmuc_symbols()    
    elif(command == 'VN30'):
        stocks = db.get_vn30_symbols()
    elif(command == 'BDS'):
        stocks = db.get_bds_symbols()
    elif(command == 'ALL'):
        stocks = db.get_all_stocks()
    print(stocks)
    rs = []    
    for symbol in stocks:
        print(symbol)
        s = Stock(name = symbol)
        p = PriceAction(symbol=s.name,df_data=s.df_data,days=10)
        rs.append([p.symbol,p.suc_bat,p.suc_bat_am,p.suc_bat+p.suc_bat_am])
    df = pd.DataFrame(rs,columns=['Symbol','Tăng','Rơi','TH'])
    df = df.sort_values(by=['TH'],ascending=False)
    df.to_excel(f'./data/{command}-{StrTODAY}.xlsx')
    return df

class DailyReport:
    def __init__(self) -> None:
        self.title = f'{StrTODAY} - [Dấu hiệu] - Big trend UP'
        self.content = self.get_daily_report()

    def get_daily_report(self):
        output = ''
        stocks = db.get_all_stocks_db()
        print(stocks)
        errors = []
        for symbol in stocks:
            try:
                s = SupperStock(name=symbol)
                if (s.has_supper_volume):
                    output += f'{s.summary()}'
            except:
                errors.append(symbol)
        print(errors)
        return output

    def updateBlog(self):
        title = self.title
        content = self.content
        blog = Blog()
        url = blog.post(title=title,content=content,tags='daily report')
        return url
    
    def __str__(self) -> str:
        return f'{self.title}\n{self.content}'

d = DailyReport()
print(d)
d.updateBlog()
print(d.updateBlog())