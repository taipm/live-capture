from Constant import *
import pandas as pd
import numpy as np
from DateHelper import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from vnstock import *

class VnindexDay:
    def __init__(self, date, close, change,volume, liquidity, volume_agree, liquidity_agree, open, high,low) -> None:
        pass

class VnIndexOrders:
    url = 'https://s.cafef.vn/Lich-su-giao-dich-VNINDEX-2.chn#data'
    def __init__(self) -> None:
        self.df_data = self.convertToCleanData()
        

    def getData(self)->pd.DataFrame:
        df_data = pd.read_html(self.url)[2].iloc[1:]
        print(df_data)
        return df_data
    
    def convertToCleanData(self)->pd.DataFrame:
        df_raw = self.getData()
        df = df_raw
        
        df['date'] = df_raw[0]
        del df[0]
        
        df['mark'] = df_raw[1].map(lambda x:x.split(' ')[0]).map(lambda y:float(y))
        df['%'] = df_raw[1].map(lambda x:x.split(' ')[1][1:]).map(lambda y:float(y))
        del df[1]

        df['count_buy'] = df_raw[2]
        del df[2]

        df['volume_buy'] = df_raw[3]
        del df[3]

        df['count_sell'] = df_raw[4]
        del df[4]

        df['volume_sell'] = df_raw[5]
        del df[5]

        df['volume_buy_and_sell'] = df_raw[8]
        del df[8]

        print(df)
        return df

    def analysis(self):
        todayMark = self.df_data['mark'][1]
        todayMargin = self.df_data['%'][1]
        output = f'VnIndex: {todayMark} [{todayMargin} %] - ({StrTODAY})'

        if todayMargin >= 3:
            output += f'\nTăng mạnh'
        elif todayMargin <=-3:
            output += f'\nGiảm mạnh'
        
        print(output)
        return output
        

class VnIndex:
    def __init__(self) -> None:
        self.url_history = 'https://s.cafef.vn/Lich-su-giao-dich-VNINDEX-1.chn#data'
        
        self.url_calendar_market = 'https://www.bsc.com.vn/bao-cao-phan-tich/lich-thi-truong'
        self.df_data = self.to_df_data()
    
    def get_current(self, command:str)->pd.DataFrame:
        commands = ['Value', 'Losers', 'Gainers', 'Volume', 'ForeignTrading', 'NewLow', 'Breakout', 'NewHigh']
        if command in commands:
            df = market_top_mover(command)
            return df
        else:
            print('Lỗi câu lệnh')
            return pd.DataFrame.empty
        

    def getTopGainers(self):
        df = market_top_mover("Gainers")
        return df
    
    def get_history_data(self):        
        df_data = pd.read_html(self.url_history)[2].iloc[2:]
        return df_data
    
    def to_df_data(self):
        df = self.get_history_data()
        df['date'] = df[0]
        del df[0]
        df['close'] = df[1]
        del df[1]
        df['change'] = df[2]
        del df[2]
        del df[3]
        df['volume'] = df[4]
        del df[4]
        df['liquidity'] = df[5].map(lambda x:float(float(x)/billion))
        del df[5]
        df['volume_agree'] = df[6]
        del df[6]
        df['liquidity_agree'] = df[7].map(lambda x:float(float(x)/billion))
        del df[7]
        df['open'] = df[8].map(lambda x:float(x))
        del df[8]
        df['high'] = df[9]
        del df[9]
        df['low'] = df[10]
        del df[10]

        df['mark'] = df['change'].map(lambda x : float(x.split(' ')[0]))
        df['%'] = df['change'].map(lambda x : float(x.split(' ')[1][1:]))
        del df['change']

        return df

    @property
    def sum_mark(self):
        return np.sum(self.df_data['mark'])
    @property
    def sum_pct(self):
        return np.sum(self.df_data['%'])

# vni = VnIndex()
# print(vni.df_data.to_markdown())
# print(vni.sum_pct)
# print(vni.get_current('Breakout'))
# print(vni.getTopGainers())

vni = VnIndexOrders()
print(vni.df_data)
vni.analysis()
#vni.getData()