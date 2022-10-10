# -*- coding: utf-8 -*-
import datetime
from requests.exceptions import HTTPError
import pandas as pd
import json
from urllib.request import urlopen
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

def Get_Intraday_Sticks(symbol):
        url = f'https://s.cafef.vn/Lich-su-giao-dich-{symbol}-6.chn#data'
        data = pd.read_html(url)
        
        df_sticks = data[len(data)-1]
        df_sticks = pd.DataFrame(df_sticks.values,columns=['Time','PriceX','Volume','Sum Volume','Percent'])

        #Tách giá
        df_sticks['Price'] = df_sticks['PriceX'].apply(lambda x: x.split(' ')[0])
        df_sticks['Price']

        df_sticks['%'] = df_sticks['PriceX'].apply(lambda x: x.split(' ')[2])
        df_sticks['%'] = df_sticks['%'].apply(lambda x: x[1:len(x)-2])

        del df_sticks['PriceX']

        #cols = ['Volume','Sum Volume','Price','%','Percent']
        cols = ['Volume','Sum Volume','Price','%']
        df_sticks[cols] = df_sticks[cols].apply(pd.to_numeric, downcast='float', errors='coerce')



        df_sticks['Time'] = df_sticks['Time'].apply(lambda x: datetime.datetime.today().strftime('%Y-%m-%d') + ' ' + str(x))
        df_sticks['Time'] = df_sticks['Time'].astype("datetime64")
        df_sticks.set_index('Time')

        df_sticks['Money'] = df_sticks['Price']*df_sticks['Volume']

        return df_sticks

        
#df = GetStockData('VND')
#print(df)

