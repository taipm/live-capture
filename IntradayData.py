#from tkinter.messagebox import RETRY
#from vnstock import *
import pandas as pd
from helpers import *
import db

def GetIntradayData(symbol):
    _page_num = 0
    _page_size = 5000
    
    df =  db.get_intraday_data(symbol=symbol, 
                            page_num=_page_num, 
                           page_size=_page_size)
    while True:
        _page_num += 1
        df_next =  db.get_intraday_data(symbol=symbol, 
                            page_num=_page_num, 
                           page_size=_page_size)
        if df_next.empty:
            print(f'page_num: {_page_num}')
            break
        
        df = df.append(df_next)
    return df

# df = GetIntradayData("HAX")
# print(df.tail(20))

class IntradayDb:
    
    def __init__(self,symbol) -> None:
        self.symbol = symbol.upper()
        self.db_file_path = './data/' + self.symbol + '-Intraday-' + StrTODAY + ".xlsx"
    
    def GetLastData(self):
        df = pd.read_excel(self.db_file_path)
        return df

    def UpdateDb(self):
        df = GetIntradayData(self.symbol)
        if(not df.empty):
            df.to_excel(self.db_file_path)

class AnalysisIntradayData:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()

        self.df_data = GetIntradayData(symbol=self.symbol)

        self.df_big_sticks = self.Get_Big_Sticks()
        self.df_big_buy_sticks = self.df_big_sticks[self.df_big_sticks['a']=='BU']
        self.df_big_sell_sticks = self.df_big_sticks[self.df_big_sticks['a']=='SD']

        self.df_buy = self.df_data[self.df_data['a']=='BU']
        self.df_sell = self.df_data[self.df_data['a']=='SD']

        self.sum_Volume_Buy = self.df_buy['volume'].sum() 
        self.sum_Volume_Sell = self.df_sell['volume'].sum()
        self.sum_Volume = self.df_data['volume'].sum()

        self.rateOf_Buy_Volume = self.sum_Volume_Buy/self.sum_Volume
        self.rateOf_Sell_Volume = self.sum_Volume_Sell/self.sum_Volume
        self.rateOf_Buy_Over_Sell_Volume = self.sum_Volume_Buy/self.sum_Volume_Sell


        self.countOf_Orders = len(self.df_data.index)
        self.countOf_BuyOrders = len(self.df_buy.index)
        self.countOf_SellOrders = len(self.df_sell.index)
        self.rateOf_Buy_Orders = self.countOf_BuyOrders/self.countOf_Orders
        self.rateOf_Sell_Orders = self.countOf_SellOrders/self.countOf_Orders
        self.rateOf_Buy_Over_Sell_Orders = self.countOf_BuyOrders/self.countOf_SellOrders

        self.db = IntradayDb(self.symbol)
        self.db.UpdateDb()

    def get_last_stick(self):
        return self.df_data.sort_values(by=['time'],ascending=False).iloc[:1]
        
    def get_top_sticks(self, n_sticks):
        return self.df_data.sort_values(by=['volume'],ascending=False).head(n_sticks)

    def analysis_top_sticks(self, n_sticks):
        df = self.get_top_sticks(n_sticks=n_sticks)
        sum_volume = df[df['a']=='BU']['volume'].sum() - df[df['a']=='SD']['volume'].sum()
        return sum_volume

    def Get_Big_Sticks(self):
        rate_of_big_stick = 20/100
        limit_money = 200000000
        df_big_sticks_by_rate = self.df_data[self.df_data['volume']>=rate_of_big_stick]
        df_big_sticks_by_rate = df_big_sticks_by_rate[df_big_sticks_by_rate['volume']*df_big_sticks_by_rate['price']>=limit_money]

        return df_big_sticks_by_rate

    def analysis_shark_action(self):
        sum_vol_big_sticks = self.df_big_sticks['volume'].sum()
        sum_vol_buy_big_sticks = self.df_big_buy_sticks['volume'].sum()
        sum_vol_sell_big_sticks = self.df_big_sell_sticks['volume'].sum()
        rateOf_buy_sell = sum_vol_buy_big_sticks/sum_vol_sell_big_sticks
        rateOf_shark = (sum_vol_big_sticks/self.sum_Volume)*100
        analysis_result = f'{rateOf_shark:,.2f} (%) - Tỷ lệ (M/B): {rateOf_buy_sell:,.2f}'

        if(rateOf_buy_sell >= 2):
            analysis_result += ' - MUA MẠNH'
        elif(rateOf_buy_sell <= 1/2):
            analysis_result += ' - BÁN MẠNH'
        else:
            analysis_result += ' - NA'        
        return analysis_result

    def GetSummary(self):
        summary_text = (
            f'Shark action: {self.analysis_shark_action()}\n'+\
            f'Volume: {self.sum_Volume:,.0f} | Rate (Buy): {self.rateOf_Buy_Volume:.2f} (%) | Rate (Buy/Sell): {self.rateOf_Buy_Over_Sell_Volume:.2f}\n'
            f'Orders: {self.countOf_Orders:,.0f} | Rate (Buy orders): {self.rateOf_Buy_Orders:.2f} (%) | Rate (Buy/Sell Orders): {self.rateOf_Buy_Over_Sell_Orders:.2f} (%)\n'
        )

        summary_text += f'Forcast: {self.symbol} - {self.GetForcast()}'
        return summary_text
       
    def GetForcast(self):
        if(self.rateOf_Buy_Over_Sell_Orders > 1) and (self.rateOf_Buy_Over_Sell_Volume > 1):
            return 'BUY'
        elif (self.rateOf_Buy_Over_Sell_Orders < 1) and (self.rateOf_Buy_Over_Sell_Volume < 1):
            return 'SELL'
        else:
            return 'NA'

    def GetMaxVolume_Buy(self):
        return self.df_buy['volume'].max()

# x = AnalysisIntradayData(symbol='VND')
# print(x.get_last_stick())
# sticks = x.get_top_sticks(10)
# print(sticks)


# top_sticks = x.analysis_top_sticks(10)
# print(top_sticks)
# print(x.GetSummary())
# df = x.Get_Big_OrderStick()
# print('Big_OrderSticks')
# print(df)
# a = IntradayDb(symbol='HAX')
# a.UpdateDb()
# print(a.GetSummary())