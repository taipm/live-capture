
from datetime import date
from Alpha import Alpha
from AnalysisPrices import AnalysisPrice
from BotTranslator import BotTranslator
from DateRange import DateRange
from FinanceStock import FinanceStock
from Stock import Stock


def Test_DateRange():
    r = DateRange(start_date=date(2022,10,1), end_date= date(2022,10,20))
    print(r.startDate)
    print(r.length)
    print(r.isInRange(date=date(2022,10,15)))
    print(r.isInRange(date=date(2022,10,25)))    
    print(r.__next__(step=2))

def Test_FinanceStock():
    f = FinanceStock(symbol='FRT')    
    print(f.get_avg_dividend())

def Test_Stock():
    stock = Stock(name='HAH')
    print(stock.summary())

def Test_AnalysisPrice():
    stock = Stock(name='HAH')
    p = AnalysisPrice(stock.prices.tolist())
    print(p)

def Test_Translator():
    t = BotTranslator(inputText="Xin chào")
    print(t.transText)

def Test_Alpha():
    a = Alpha(query="How far from earth to moon")
    print(a.answerText)

    a = Alpha(query="Khoảng cách từ trái đất đến mặt trăng")
    print(a.answerText)

def runTest():
    Test_DateRange()
    Test_FinanceStock()
    Test_Stock()
    Test_AnalysisPrice()
    Test_Translator()
    Test_Alpha()


runTest()