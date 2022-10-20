# -*- coding: utf-8 -*-
import datetime
from requests.exceptions import HTTPError
import pandas as pd
import json
from urllib.request import urlopen
import requests
from pandas import json_normalize
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_stock_data_from_api(symbol):
        url = "https://stock.kdtv4.vn/api/app/company/by-stock-code?stockCode=" + symbol.upper()        
        try:
                response = urlopen(url)                
                data_json = json.loads(response.read())
                                
                df = pd.json_normalize(data_json['companyStocks'])
                df = df[['stockCode','giaTriTangGiam','phanTramTangGiam','dongCua','khoiLuong','moCua','caoNhat','thapNhat','giaoDichThoaThuan','nuocNgoaiMua','nuocNgoaiBan','postedDate']]        
        
                df['Date'] = pd.to_datetime(df['postedDate']).dt.date#,format='%Y%m%d', errors='ignore')
                df = df.sort_values(['Date'], ascending=False)
                del df['postedDate']
                                
                df['Stock'] = df['stockCode']
                del df['stockCode']

                df['+/-'] = df['giaTriTangGiam']
                del df['giaTriTangGiam']

                df['%'] = df['phanTramTangGiam']
                del df['phanTramTangGiam']

                df['Close'] = df['dongCua']
                del df['dongCua']

                df['Volume'] = df['khoiLuong']
                del df['khoiLuong']

                df['Open'] = df['moCua']
                del df['moCua']

                df['High'] = df['caoNhat']
                del df['caoNhat']

                df['Low'] = df['thapNhat']
                del df['thapNhat']

                df['NN Mua'] = df['nuocNgoaiMua']
                del df['nuocNgoaiMua']

                df['NN Ban'] = df['nuocNgoaiBan']
                del df['nuocNgoaiBan']

                df['GDTT'] = df['giaoDichThoaThuan']
                del df['giaoDichThoaThuan']

                #STEP 2: MỞ RỘNG DỮ LIỆU
                df['Money'] = (df['Close']*df['Volume']*1000*100)/1000000000 #Giá trị giao dịch (tỷ)
                df['NN'] = df['NN Mua'] - df['NN Ban']
                df['M(NN)'] = df['NN']*df['Volume']*1000*100/1000000000 #Giá trị giao dịch của khối ngoại (tỷ)

                df = df.drop_duplicates(subset=['Date'])                
                return df
        except: #Cổ phiếu chưa có trong danh mục
                return pd.DataFrame()

def GetStockData(symbol):    
        data = get_stock_data_from_api(symbol=symbol)
        if not data.empty:
                df = pd.DataFrame(data=data)                     
                df = df.reset_index(drop=True)
                df.set_index('Date')
                return df
        else:
                print('Cổ phiếu chưa có trong danh mục')
                return pd.DataFrame()        

# def Get_Intraday_Sticks(symbol):
#         url = f'https://s.cafef.vn/Lich-su-giao-dich-{symbol}-6.chn#data'
#         data = pd.read_html(url)
        
#         df_sticks = data[len(data)-1]
#         df_sticks = pd.DataFrame(df_sticks.values,columns=['Time','PriceX','Volume','Sum Volume','Percent'])

#         #Tách giá
#         df_sticks['Price'] = df_sticks['PriceX'].apply(lambda x: x.split(' ')[0])
#         df_sticks['Price']

#         df_sticks['%'] = df_sticks['PriceX'].apply(lambda x: x.split(' ')[2])
#         df_sticks['%'] = df_sticks['%'].apply(lambda x: x[1:len(x)-2])

#         del df_sticks['PriceX']

#         #cols = ['Volume','Sum Volume','Price','%','Percent']
#         cols = ['Volume','Sum Volume','Price','%']
#         df_sticks[cols] = df_sticks[cols].apply(pd.to_numeric, downcast='float', errors='coerce')



#         df_sticks['Time'] = df_sticks['Time'].apply(lambda x: datetime.datetime.today().strftime('%Y-%m-%d') + ' ' + str(x))
#         df_sticks['Time'] = df_sticks['Time'].astype("datetime64")
#         df_sticks.set_index('Time')

#         df_sticks['Money'] = df_sticks['Price']*df_sticks['Volume']

#         return df_sticks

def get_intraday_data(symbol, page_num, page_size):
    """
    This function returns the stock realtime intraday data.
    Args:
        symbol (:obj:`str`, required): 3 digits name of the desired stock.
        page_size (:obj:`int`, required): the number of rows in a page to be returned by this query, suggest to use 5000.
        page_num (:obj:`str`, required): the page index starting from 0.
    Returns:
        :obj:`pandas.DataFrame`:
        | tradingDate | open | high | low | close | volume |
        | ----------- | ---- | ---- | --- | ----- | ------ |
        | YYYY-mm-dd  | xxxx | xxxx | xxx | xxxxx | xxxxxx |
    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
    """
    d = datetime.now()
    if d.weekday() > 4: #today is weekend
        data = requests.get('https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/{}/his/paging?page={}&size={}&headIndex=-1'.format(symbol, page_num, page_size, headers={'Cache-Control': 'no-cache'})).json()
    else: #today is weekday
        data = requests.get('https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/{}/his/paging?page={}&size={}'.format(symbol, page_num, page_size),headers={'Cache-Control': 'no-cache'}).json()
    df = json_normalize(data['data']).rename(columns={'p':'price', 'v':'volume', 't': 'time'})
    return df

def GetIntradayData(symbol):
    _page_num = 0
    _page_size = 5000
    
    df =  get_intraday_data(symbol=symbol, 
                            page_num=_page_num, 
                           page_size=_page_size)
    
    while True:
        _page_num += 1
        df_next =  get_intraday_data(symbol=symbol, 
                            page_num=_page_num, 
                           page_size=_page_size)
        if df_next.empty:
            break
        else:
            df = df.append(df_next)
    return df

def get_now_price(symbol):
    df_data = GetIntradayData(symbol = symbol)
    price = None
    if (df_data.empty):
        price = get_stock_data_from_api(symbol=symbol).iloc[0]['Close']*1000
    else:
        price = df_data.sort_values(by=['time'],ascending=False).iloc[:1]['price'].values[0]
    
    return price


#print(get_now_price("HPG"))
# print(get_now_price_2("HPG"))