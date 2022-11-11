from PriceAction import PriceAction
from Stock import *
from db import *
import pandas as pd

# def get_all_stocks_to_buy():
#     lst = []
#     stocks = db.get_all_stocks()
#     #stocks = stocks[30:60]
#     for stock in stocks:
#         try:
#             s = Stock(name=stock)
#             s.Prepare()
#             pivots = s.get_pivots_as_string()
#             if(len(pivots)>0):
#                 lst.append([stock,pivots])
#                 #print(s.get_pivots_as_string())
#         except:
#             x=1

#     print(lst)
#     df = pd.DataFrame(lst, columns=['symbokl','pivots'])
#     df.to_excel('Pivots.xlsx')

# def get_all_stocks_to_buy_2(fileName):
#     lst = []
#     stocks = db.get_all_stocks()
#     #stocks = stocks[30:60]
#     for stock in stocks:
#         try:
#             s = Stock(name=stock)            
#             pivots = s.get_pivots()

#             if(len(pivots)>0):
                
#                 indexs = []
#                 for pivot in pivots:
#                     print(f'{pivot.to_string()}')
#                     indexs.append(pivot.index)
#                 lst.append([stock,indexs])
#                 #print(s.get_pivots_as_string())
#             #print(f'{stock} - {pivots}')
#         except:
#             x=1

#     print(lst)
#     df = pd.DataFrame(lst, columns=['Symbol','Pivots'])
#     df.to_excel(fileName)

# def get_all_stocks_min_vol(fileName):
#     lst = []
#     #stocks = db.get_all_stocks()[10:30]
#     stocks = ['BID']
#     #stocks = stocks[30:60]
#     for stock in stocks:
#         try:
#             s = Stock(name=stock)
#             s.Prepare()
#             rs = s.get_min_vols()
#             print(rs)
#             if(len(rs)>0):
#                 indexs = []
#                 for pivot in rs:
#                     print(f'{pivot.to_string()}')
#                     indexs.append(pivot.index)
#                 lst.append([stock,indexs])
#                 #print(s.get_pivots_as_string())
#             #print(f'{stock} - {pivots}')
#         except:
#             x=1

#     print(lst)
#     df = pd.DataFrame(lst, columns=['Symbol','Pivots'])
#     df.to_excel(fileName)

# file_name = StrTODAY + '-Pivots.xlsx'
# get_all_stocks_to_buy_2(fileName=file_name)
# file_name = StrTODAY + '-min-vols.xlsx'
# get_all_stocks_min_vol(fileName=file_name)

# s = Stock(name='BID')
# rs = s.get_min_vols()
# for item in rs:
#     print(item.to_string())
#get_all_stocks_to_buy()


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
    
    # banks = db.get_banks_symbols()
    # rs = []
    # for bank in banks:
    #     print(f'Đang xử lý {bank}')
    #     s = Stock(name = bank)
    #     p = PriceAction(symbol=s.name,df_data=s.df_data,days=10)

    #     rs.append([p.symbol,p.suc_bat])
    # df = pd.DataFrame(rs,columns=['Symbol','Sức mạnh'])
    # df = df.sort_values(by=['Sức mạnh'],ascending=False)
    # return df