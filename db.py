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
from vnstock import *
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

def get_stock_data_from_api(symbol):
        url = "https://stock.kdtv4.vn/api/app/company/by-stock-code?stockCode=" + symbol.upper()        
        try:
                response = urlopen(url)                
                data_json = json.loads(response.read())
                                
                df = pd.json_normalize(data_json['companyStocks'])
                df = df[['stockCode','giaTriTangGiam','phanTramTangGiam','dongCua',
                        'khoiLuong','moCua','caoNhat','thapNhat','giaoDichThoaThuan','nuocNgoaiMua','nuocNgoaiBan','postedDate']]        
        
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
                df['Money'] = (df['Close']*df['Volume']*1000)
                df['NN'] = df['NN Mua'] - df['NN Ban']
                df['M(NN)'] = df['NN']*df['Volume']*1000*100 #Giá trị giao dịch của khối ngoại (tỷ)
                df['Oscillation'] = np.abs(((df['Low']-df['High'])/df['Low'])*100)
                df['Oscillation-Low-Open'] = ((df['Low']-df['Open'])/df['Open'])*100
                df['Oscillation-Open-High'] = ((df['High']-df['Open'])/df['Open'])*100

                df = df.drop_duplicates(subset=['Date'])                
                return df
        except: #Cổ phiếu chưa có trong danh mục
                return pd.DataFrame()

def GetStockData(symbol):    
        data = get_stock_data_from_api(symbol=symbol)
        if not data.empty:
                df = pd.DataFrame(data=data)
                df['Close'] = df['Close']
                df = df.reset_index(drop=True)
                df.set_index('Date')
                return df
        else:
                print(f'{symbol} - chưa có trong danh mục')
                return pd.DataFrame()

def test_Oscillation():
    symbol = 'VND'
    data = GetStockData(symbol=symbol).iloc[0]
    high = data['High']
    low = data['Low']
    open = data['Open']
    osci_open = data['Oscillation-Low-Open']

    print(f'L {low} : O {open} -> {open-low:,.2f} : {osci_open:,.2f}')

#test_Oscillation()


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

def get_banks_symbols():
    bank_list = ['VPB', 'BID','CTG','VCB','TCB',
                'TPB','VIB','MBB','ACB','EIB','STB',
                'BVB','NAB','LPB']
    return bank_list

def get_banks_symbols_command():
    bank_list = ['VPB', 'BID','CTG','VCB','TCB',
                'TPB','VIB','MBB','ACB','EIB','STB',
                'BVB','NAB','LPB']
    output = ','.join(bank_list)
    return output

def get_securities_symbols():
    lst = ['VCI','SSI','VND','BSI','CTS','TVS',
        'FTS','SHS','VIX']
    ouput = ','.join(lst)

    return ouput

def get_vn30_symbols():
    lst = ['PLX','VCB','HPG','FPT','VPB',
            'SAB','POW','GVR','STB','SSI',
            'MBB','TCB','ACB','VHM','TPB',
            'VIB','CTG','BID','VRE','NVL',
            'MSN','VIC','PDR','KDH','HDB',
            'PNJ'
            ]
    ouput = ','.join(lst)

    return ouput

def get_all_stocks():
    stocks = listing_companies()['ticker']
    return stocks.to_list()

def get_vn30_symbols_as_command():
    lst = get_vn30_symbols()
    ouput = ','.join(lst)
    return ouput

def get_bds_symbols():
    lst = ['PDR','VHM','DXG','SCR','KDH',
            'CII','NBB','CEO','DIG','NVL',
            #'NLG','VRE','ACB','VHM','TPB',
            'DPR','PHR','BCM'
            #'VIB','CTG','BID','VRE','NVL',
            #'MSN','VIC','PDR','KDH','HDB'
            ]

    return lst

def get_bds_symbols_as_command():
    lst = ['PDR','VHM','DXG','SCR','KDH',
            'CII','NBB','CEO','DIG','NVL',
            'NLG','VRE','ACB','VHM','TPB',
            #'VIB','CTG','BID','VRE','NVL',
            #'MSN','VIC','PDR','KDH','HDB'
            ]
    ouput = ','.join(lst)

    return ouput

def get_danhmuc_symbols():
    lst = ['VND','HAX','PDR','SCR','DXG',
            'HPG','FPT','FRT','VCI','TPB',
            'BID','BSI','MSH','VIB','HBC',
            'IDC','NLG','BSR','ASM','SSI',
            'PDR'
            #'MSN','VIC','PDR','KDH','HDB'
            ]
    ouput = ','.join(lst)

    return ouput

#print(get_now_price("HPG"))
# print(get_now_price_2("HPG"))