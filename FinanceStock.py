from cmath import cos
import math
from vnstock import *

#Compound: Lãi kép
def compound_share(beginValue = 100, rate = 0.1, repeatedTime = 1):
    sum = beginValue

    for i in range(0,repeatedTime):
        sum += sum*rate
        sum = math.floor(sum)
        print(f'{i} - {sum}')

    return sum
    
#x = compound_share(beginValue = 100, rate = 0.1, repeatedTime = 5)

class FinanceStock:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()

    def getBasicInfo(self):
        #df = dividend_history(self.symbol)
        #df = stock_ls_analysis("TCB, BID, CEO, GMD")
        #query = '"'+self.symbol + ", " + self.symbol+'"'
        query = self.symbol
        if (self.symbol == "WCS"):
            query = self.symbol + ", DSN"
        else:
            query = self.symbol + ", WCS"
        #print(query)
        df = stock_ls_analysis(query)
        df = df[df['ticker'] == self.symbol]
        df = df[['ticker','rsi','dividend','priceToBook']]
        return df

    def getDividend(self):

        df = dividend_history(self.symbol)
        print(df)
        df_cash = df[df['issueMethod']=='cash']#['cashDividendPercentage']
        df_share = df[df['issueMethod']=='share']#['cashDividendPercentage']

        start_year = df['cashYear'].min()
        end_year = df['cashYear'].max()

        sum_of_year = end_year-start_year

        default_shares = 100
        sum_shares = default_shares
        sum_cash = 0

        count_year = 0
        for i in range(start_year,end_year):
            year = start_year + count_year
            print(f'Start: {start_year} End {end_year} - Now: {year} count_year: {count_year}')
            rate_of_cash = df_cash[df_cash['cashYear'] == year]['cashDividendPercentage']
            rate_of_share = df_share[df_share['cashYear'] == year]['cashDividendPercentage']

            print(f'{year} - Cổ tức TM: {rate_of_cash} Cổ tức CP : {rate_of_share}')
            print(f'{year} - Cổ tức CP {rate_of_share} Cổ tức TM : {rate_of_cash}')

            sum_cash += sum_shares*rate_of_cash
            sum_shares += sum_shares*rate_of_share
            #sum_shares = math.floor(sum_shares)

            count_year+=1


        share_avg = sum_shares/sum_of_year
        cash_avg = sum_cash/sum_of_year

        return f'Years: {sum_of_year} -  share-avg: {share_avg:.2f} - cash-avg: {cash_avg:.2f}'

# stock = 'PVT'
# f = FinanceStock(symbol=stock)
# # x = f.getBasicInfo()

# #print(f.getDividend())

# x = valuation_rating(stock)
# print(x)


# print(price_board("PVT").to_markdown())
# print(price_board('PVT').transpose())