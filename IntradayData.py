from DateHelper import *
from Caculator import *
from IntradayDb import IntradayDb
from db import *
from Constant import *

class AnalysisIntradayData:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.hasError = True
        self.df_data = self.loadData()
        
        if not self.hasError:
            self.las_stick = self.df_data.sort_values(by=['time'],ascending=False).iloc[:1]
            self.last_price = self.las_stick['price'][0]/1000
            self.df_big_sticks = self.Get_Big_Sticks()
            self.df_big_buy_sticks = self.df_big_sticks[self.df_big_sticks['a']=='BU']
            self.df_big_sell_sticks = self.df_big_sticks[self.df_big_sticks['a']=='SD']

            self.df_buy = self.df_data[self.df_data['a']=='BU']
            self.df_sell = self.df_data[self.df_data['a']=='SD']

            self.sum_Volume = self.df_data['volume'].sum()

            self.rateOf_Buy_Volume = self.sum_vol_buy/self.sum_Volume
            self.rateOf_Sell_Volume = self.sum_vol_sell/self.sum_Volume

            self.countOf_Orders = len(self.df_data.index)
            self.countOf_BuyOrders = len(self.df_buy.index)
            self.countOf_SellOrders = len(self.df_sell.index)

            self.rateOf_Buy_Orders = self.countOf_BuyOrders/self.countOf_Orders
            self.rateOf_Sell_Orders = self.countOf_SellOrders/self.countOf_Orders

            self.db = IntradayDb(self.symbol)
            self.db.UpdateDb()
        else:
            self.las_stick = None 
            self.last_price = None
            self.df_big_sticks = None
            self.df_big_buy_sticks = None
            self.df_big_sell_sticks = None 

            self.df_buy = None 
            self.df_sell = None

            self.sum_Volume = 0

            self.rateOf_Buy_Volume = 0
            self.rateOf_Sell_Volume =0

            self.countOf_Orders = 0
            self.countOf_BuyOrders = 0
            self.countOf_SellOrders = 0

            self.rateOf_Buy_Orders = 0
            self.rateOf_Sell_Orders = 0
    
    def loadData(self):
        df = GetIntradayData(symbol=self.symbol)
        if(df.empty or df is None):
            print(f'{self.symbol} - KHÔNG LẤY ĐƯỢC DỮ LIỆU TRONG NGÀY')
            self.hasError = False
        return df

    @property
    def rateOf_Buy_Over_Sell_Volume(self):
        if(self.sum_vol_sell > 0):
            return self.sum_vol_buy/self.sum_vol_sell
        else:
            return 100
    @property
    def rateOf_Buy_Over_Sell_Orders(self):
        if(self.countOf_SellOrders > 0):
            return self.countOf_BuyOrders/self.countOf_SellOrders
        else:
            return 100
    @property
    def avg_price(self):
        avg_price = (np.sum(self.df_data['volume']*self.df_data['price']))/np.sum(self.df_data['volume'])/1000
        return avg_price

    @property
    def rate_of_shark(self):
        return (self.vol_of_shark/self.sum_Volume)*100

    @property
    def vol_of_shark(self):
        return self.df_big_sticks['volume'].sum()

    @property
    def vol_of_shark_buy(self):
        if self.hasError:
            return 0
        else:
            return self.df_big_buy_sticks['volume'].sum()

    @property
    def vol_of_shark_sell(self):
        return self.df_big_sell_sticks['volume'].sum()

    @property
    def rate_of_active_buy(self):
        return self.sum_vol_buy/self.sum_Volume

    @property
    def sum_vol_buy(self):
        return self.df_buy['volume'].sum()
    
    @property
    def sum_vol_sell(self):
        return self.df_sell['volume'].sum()
    
    @property
    def sum_vol_net_buy(self):
        return self.sum_vol_buy-self.sum_vol_sell

    @property
    def liquidity(self):
        liquidity = np.sum(self.df_data['price']*self.df_data['volume'])/billion #Tỷ
        return liquidity

    @property
    def liquidity_of_shark(self):
        liquidity = np.sum(self.df_big_sticks['price']*self.df_big_sticks['volume'])/billion #Tỷ
        return liquidity

    def get_top_sticks(self, n_sticks):
        return self.df_data.sort_values(by=['volume'],ascending=False).head(n_sticks)
    
    def get_top_sticks_markdown(self,n_sticks):
        df = self.get_top_sticks(n_sticks=n_sticks)

        df = df[['price','volume','a','time']]
        sum_buy = df[df['a']=='BU']['volume'].sum()
        sum_sell = df[df['a']=='SD']['volume'].sum()

        output = df.to_markdown() + "\n" + f'Volume (M-B): {self.sum_vol_buy-self.sum_vol_sell:,.2f} ~ {(sum_buy-sum_sell)*self.avg_price*1000:,.2f}'
        
        if(sum_buy/sum_sell >=1.2):
            output += ' => Đang mua vào'
        elif(sum_sell/sum_buy >= 1.2):
            output += ' => Đang bán ra'
        else:
            output += ' => Chưa rõ xu hướng'
        output += '\n'
        return output

    def analysis_top_sticks(self, n_sticks):
        df = self.get_top_sticks(n_sticks=n_sticks)
        sum_volume = df[df['a']=='BU']['volume'].sum() - df[df['a']=='SD']['volume'].sum()
        return sum_volume

    def Get_Big_Sticks(self):
        rate_of_big_stick = 20/100
        limit_money = 200000000
        df_big_sticks_by_rate = self.df_data[self.df_data['volume']>=rate_of_big_stick]
        df_big_sticks_by_rate = df_big_sticks_by_rate[df_big_sticks_by_rate['volume']*df_big_sticks_by_rate['price']>=limit_money].sort_values(by=['volume'],ascending=False)

        return df_big_sticks_by_rate

    def analysis_shark_action(self):
        if self.hasError:
            return 'Lỗi. Không lấy được dữ liệu trong ngày'
        else:
            rateOf_buy_sell = self.vol_of_shark_buy/self.vol_of_shark
            analysis_result = f'Shark'+\
                f'\n(Money): {self.liquidity_of_shark:,.2f} | (volume): {self.vol_of_shark:,.0f}'+\
                f'\nTỷ lệ vol: {self.rate_of_shark:,.2f} (%) - Tỷ lệ (M/B): {rateOf_buy_sell:,.2f}'

            if(rateOf_buy_sell >= 2):
                analysis_result += ' - MUA MẠNH'
            elif(rateOf_buy_sell <= 1/2):
                analysis_result += ' - BÁN MẠNH'
            else:
                analysis_result += ' - NA'
            return analysis_result

    def summary(self):
        if self.hasError:
            return 'LỖI. KHÔNG LẤY ĐƯỢC DỮ LIỆU TRONG NGÀY'
        else:
            summary_text = (
                f'\n-Intraday: '
                f'{self.symbol} - Giá TB: {self.avg_price:,.2f} | Giá HT {self.last_price:,.2f} ~ {percent(self.last_price,self.avg_price):,.2f} (%)'
                f'\nThanh khoản: {self.liquidity:,.2f}'
                f'\nKL: {self.sum_Volume:,.0f} | Rate (Buy): {self.rateOf_Buy_Volume:.2f} (%) | Rate (Buy/Sell): {self.rateOf_Buy_Over_Sell_Volume:.2f}'
                f'\nSố lệnh: {self.countOf_Orders:,.0f} | TL lệnh mua: {self.rateOf_Buy_Orders:.2f} (%)'
                f'\nDự báo: {self.symbol} - {self.GetForecast()}'
                f'\nMua/bán chủ động: {self.sum_vol_buy:,.0f} | {self.sum_vol_sell:,.0f} | Tỷ lệ {self.rate_of_active_buy:,.2f}'
                f'\n{self.analysis_shark_action()}'
                f'\nTop sticks:'
                f'\n{self.get_top_sticks_markdown(10)}'
            )
            return summary_text
       
    def GetForecast(self):
        if(self.rateOf_Buy_Over_Sell_Orders > 1) and (self.rateOf_Buy_Over_Sell_Volume > 1):
            return 'BUY'
        elif (self.rateOf_Buy_Over_Sell_Orders < 1) and (self.rateOf_Buy_Over_Sell_Volume < 1):
            return 'SELL'
        else:
            return 'NA'

