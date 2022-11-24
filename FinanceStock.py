
from unicodedata import name
from vnstock import *

class FinanceStock:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()        

    def __get_dividend_history(self):
        return dividend_history(self.symbol)
    
    def get_avg_dividend(self):
        df = self.__get_dividend_history()

        df_cash = df[df['issueMethod']=='cash']
        df_share = df[df['issueMethod']=='share']

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