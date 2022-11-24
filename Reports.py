from PriceAction import PriceAction
from Stock import *
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

