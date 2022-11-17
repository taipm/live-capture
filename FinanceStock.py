
from unicodedata import name
from vnstock import *
from DateHelper import percent

class FinanceStock:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.df_basic_data = self.GetTCB()
        
        self.Price = self.df_basic_data['Giá Khớp Lệnh'][0]
        self.RSI = self.df_basic_data['RSI'][0]
        self.ROE = self.df_basic_data['ROE'][0]*100
        self.PE = self.df_basic_data['P/E'][0]
        self.PB = self.df_basic_data['P/B'][0]
        self.MA20 = self.df_basic_data['MA20'][0]
        self.MA50 = self.df_basic_data['MA50'][0]
        self.MA100 = self.df_basic_data['MA100'][0]
        self.signal_KT = self.df_basic_data['Tín hiệu KT'][0]
        self.signal_TBD = self.df_basic_data['Tín hiệu TB động'][0]
        self.MACD_Signal = self.df_basic_data['MACD Signal'][0]
        self.MACD_Volume = self.df_basic_data['MACD Volume'][0]
        self.Du_Mua = self.df_basic_data['Khối lượng Dư mua'][0]
        self.Du_Ban = self.df_basic_data['Khối lượng Dư bán'][0]
        self.Price_At_Max_Vol = self.df_basic_data['Khớp nhiều nhất'][0]
        self.Evalue_Price = self.df_basic_data['TCBS định giá'][0]
        
    def get_basic_analysis(self):
        return self.df_basic_data

    @property
    def rsi_review(self):
        if self.RSI <= 30:
            return f'RSI: {self.RSI:,.2f} : Quá bán'
        elif self.RSI >= 90:
            return f'RSI: {self.RSI:,.2f} : Quá mua'
        elif self.RSI >= 75:
            return f'RSI: {self.RSI:,.2f} : Đang mạnh (Mark Minervini) - Xem xét'
        else:
            return f'RSI: {self.RSI:,.2f} : Chưa xác định'

    def GetTCB(self):
        data = price_board(self.symbol)
        return data

    def get_dividend_history(self):
        return dividend_history(self.symbol)
    
    def get_avg_dividend(self):

        df = self.get_dividend_history()

        df_cash = df[df['issueMethod']=='cash']#['cashDividendPercentage']
        df_share = df[df['issueMethod']=='share']#['cashDividendPercentage']

        start_year = df['cashYear'].min()
        end_year = df['cashYear'].max()+1

        sum_of_year = end_year - start_year

        self.default_shares = 100
        sum_shares = self.default_shares
        sum_cash = 0

        count_year = 0

        for i in range(start_year,end_year):
            year = start_year + count_year
            rate_of_cash = df_cash[df_cash['cashYear'] == year]['cashDividendPercentage'].sum()
            rate_of_share = df_share[df_share['cashYear'] == year]['cashDividendPercentage'].sum()
            sum_cash += sum_shares*rate_of_cash
            sum_shares += sum_shares*rate_of_share
            
            print(f'{year} - Cổ tức TM: {sum_cash*10000:,.2f} Tổng số CP : {sum_shares:,.0f}')
            count_year+=1

        share_avg = (sum_shares-self.default_shares)/sum_of_year
        cash_avg = sum_cash/sum_of_year
        self.avg_cash = cash_avg
        self.avg_share = share_avg

        return f'Years: {sum_of_year} -  shares-avg: {share_avg:.2f} - cash-avg: {cash_avg:.2f}'

    # def get_ROI(self, price):
    #     money = self.default_shares*price


# stock = 'HPG'
# f = FinanceStock(symbol=stock)
# print(f.basic_review)
# print(f.get_signals())
# print(f.RSI)
# print(f.Price)
#print(f.get_basic_analysis())
# print(f.getBasicInfo())
# print(f.get_avg_dividend())

# x = valuation_rating(stock)
# print(x)


# print(price_board("PVT").to_markdown())
# print(price_board('PVT').transpose())