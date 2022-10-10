from vnstock import *
import pandas as pd
from helpers import *

def GetIntradayData(symbol):
    _page_num = 0
    _page_size = 5000
    
    df =  stock_intraday_data(symbol=symbol, 
                            page_num=_page_num, 
                           page_size=_page_size)
    while True:
        _page_num += 1
        df_next =  stock_intraday_data(symbol=symbol, 
                            page_num=_page_num, 
                           page_size=_page_size)
        if df_next.empty:
            print(_page_num)
            break
        
        df = df.append(df_next)
    return df

#df = GetIntradayData("VND")
#print(df.tail(20))

class AnalysisIntradayData:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()

        self.df_data = GetIntradayData(symbol=symbol)
        
        self.df_buy = self.df_data[self.df_data['a']=='BU']
        self.df_sell = self.df_data[self.df_data['a']=='SD']

        self.sum_Volume_Buy = self.df_data[self.df_data['a']=='BU']['volume'].sum()
        self.sum_Volume_Sell = self.df_data[self.df_data['a']=='SD']['volume'].sum()
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
    
    def isBig_Buy_Order(self):
        pass
    def isBig_Sell_Order(self):
        pass


         
    def GetSummary(self):
        summary_text = (
            f'Volume: {self.sum_Volume:,.0f} | Rate (Buy): {self.rateOf_Buy_Volume:.2f} (%) | Rate (Buy/Sell): {self.rateOf_Buy_Over_Sell_Volume:.2f} (%)\n'
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

class IntradayDb:
    
    def __init__(self,symbol) -> None:
        self.symbol = symbol.upper()
        self.db_file_path = './data/' + self.symbol + '-Intraday-' + StrTODAY + ".xlsx"
    
    def GetLastData(self):
        df = pd.read_excel(self.db_file_path)
        return df

    def UpdateDb(self):
        df = GetIntradayData(self.symbol)
        print(df)
        if(df != None):
            df.to_excel(self.db_file_path)

#a = AnalysisIntradayData(symbol='hax')
# a = IntradayDb(symbol='HAX')
# a.UpdateDb()
# print(a.GetSummary())