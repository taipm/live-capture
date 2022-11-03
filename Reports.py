from Stock import *
from db import *

def get_all_stocks_to_buy():
    lst = []
    stocks = db.get_all_stocks()
    #stocks = stocks[30:60]
    for stock in stocks:
        try:
            s = Stock(name=stock)
            s.Prepare()
            pivots = s.get_pivots_as_string()
            if(len(pivots)>0):
                lst.append([stock,pivots])
                #print(s.get_pivots_as_string())
        except:
            x=1

    print(lst)
    df = pd.DataFrame(lst, columns=['symbokl','pivots'])
    df.to_excel('Pivots.xlsx')

def get_all_stocks_to_buy_2(fileName):
    lst = []
    stocks = db.get_all_stocks()
    #stocks = stocks[30:60]
    for stock in stocks:
        try:
            s = Stock(name=stock)
            s.Prepare()
            pivots = s.get_pivots()

            if(len(pivots)>0):
                
                indexs = []
                for pivot in pivots:
                    print(f'{pivot.to_string()}')
                    indexs.append(pivot.index)
                lst.append([stock,indexs])
                #print(s.get_pivots_as_string())
            #print(f'{stock} - {pivots}')
        except:
            x=1

    print(lst)
    df = pd.DataFrame(lst, columns=['Symbol','Pivots'])
    df.to_excel(fileName)

def get_all_stocks_min_vol(fileName):
    lst = []
    #stocks = db.get_all_stocks()[10:30]
    stocks = ['BID']
    #stocks = stocks[30:60]
    for stock in stocks:
        try:
            s = Stock(name=stock)
            s.Prepare()
            rs = s.get_min_vols()
            print(rs)
            if(len(rs)>0):
                indexs = []
                for pivot in rs:
                    print(f'{pivot.to_string()}')
                    indexs.append(pivot.index)
                lst.append([stock,indexs])
                #print(s.get_pivots_as_string())
            #print(f'{stock} - {pivots}')
        except:
            x=1

    print(lst)
    df = pd.DataFrame(lst, columns=['Symbol','Pivots'])
    df.to_excel(fileName)

# file_name = StrTODAY + '-Pivots.xlsx'
# get_all_stocks_to_buy_2(fileName=file_name)
# file_name = StrTODAY + '-min-vols.xlsx'
# get_all_stocks_min_vol(fileName=file_name)

# s = Stock(name='BID')
# rs = s.get_min_vols()
# for item in rs:
#     print(item.to_string())
#get_all_stocks_to_buy()