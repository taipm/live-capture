
from datetime import date
from Alpha import Alpha
from AnalysisList import AnalysisList
from AnalysisPrices import AnalysisPrice
from BotAnswer import BotAnswer
from BotTranslator import BotTranslator
from BuyOrder import BuyOrder
from DailyReport import DailyReport
from DateData import DateData
from DateRange import DateRange
from DividendStock import DividendStock
from IntradayData import AnalysisIntradayData
from MongoDb import MongoDb
from Notes import Note, NoteDb
from OrderDb import OrderDb
from RichNumber import RichNumber
from SellOrder import SellOrder
from Stock import Stock
from StockOwners import StockOwners
from TextBuilder import TextBuilder
from Viewers import ViewOrders
from VnDate import VnDate
from StockNews import StockNews, StockNewsFromBSC, StockNewsFromCafeF
from vnstock import *

def Test_DateRange():
    r = DateRange(start_date=date(2022,10,1), end_date= date(2022,10,20))
    print(r.startDate)
    print(r.length)
    print(r.isInRange(date=date(2022,10,15)))
    print(r.isInRange(date=date(2022,10,25)))    
    print(r.__next__(step=2))

def Test_DividendStock():
    f = DividendStock(symbol='FRT')    
    print(f.get_avg_dividend())

def Test_Stock():
    stock = Stock(name='HAH')
    print(stock.df_data)
    print(stock.summary())

def Test_AnalysisPrice():
    stock = Stock(name='HAH')
    p = AnalysisPrice(stock.prices.tolist())
    print(p)

def Test_Translator():
    t = BotTranslator(inputText="Xin chào")
    print(t.transText)

    t = BotTranslator(inputText="Hello world")
    print(t.transText)

    t = BotTranslator(inputText="Cuộc sống thật khó khăn")
    print(t.transText)

def Test_Alpha():

    a = Alpha(query='Có bao nhiêu quốc gia trên thế giới')
    print(a.answerText)

    a = Alpha(query="How far from earth to moon")
    print(a.answerText)

    a = Alpha(query="Khoảng cách từ trái đất đến mặt trăng")
    print(a.answerText)
    a.addToNotes()

def Test_OrderDb():
    o = OrderDb()
    print(o.getStockOrdersByToday())
    print(o.getStockOrders(symbol='VND'))

    b = BuyOrder(symbol='VPG',volume=100,price=7000)
    o.addItem(b)

    s = SellOrder(symbol='VPG',volume=100,price=1000)
    o.addItem(s)

    print(o.getStockOrdersByToday().to_markdown())

def Test_VnDate():
    v = VnDate(_date=date(2002,10,1))
    print(v)
    print(v.next)
    print(v.previous)
    print(f'Weekend: {v.isWeekend}')

def Test_AnalysisIntradayData():
    t = AnalysisIntradayData(symbol='MWG')
    print(t.df_data)
    a = AnalysisList(t.df_data['price'].to_list())
    print(a)
    v = AnalysisList(t.df_data['volume'].to_list())
    print(v)

def Test_DailyReport():
    d = DailyReport()
    print(d)
    d.updateBlog()
    print(d.updateBlog())

def Test_MongoDb():
    db = MongoDb(name='Notes')
    print(db)
    print(db.getAll())
    print(db.getItemsOfToday())

def Test_TextBuilder():
    b = TextBuilder('Hello, how are you ?. Thanks. I"m 20 years old')
    print(b.words)
    print(b.text_markdown)
    print(b)

def Test_StockOwners():
    so = StockOwners(symbol='HAX')
    print(so)


def Test_StockNews():
    symbol = 'HAX'
    s_cafeF = StockNewsFromCafeF(symbol=symbol).getNews()
    for item in s_cafeF:
        print(item)
    
    print(f'{"*"*30}')
    s_cafeF = StockNewsFromCafeF(symbol=symbol).getNewsInMonth()
    for item in s_cafeF:
        print(item)

    print(f'{"--"*10}')
    s_bsc = StockNewsFromBSC(symbol=symbol).get_news()
    print(s_bsc)
    
    
    s = StockNews("DIG").getNews()
    for item in s:
        print(item)
    
    #print(s.getNews())

def Test_BotAnswer():
    bot = BotAnswer('HPG, VND, FRT')
    stocks = ['HPG, VND, FRT']
    bot.answer_stocks(stocks=stocks)

def Test_BotAnswerObj(symbol):
    return BotAnswer(symbol).answer()

def Test_RichNumber():
    print(RichNumber(77.4).rich_text)
    print(RichNumber(8750000).toText())
    print(RichNumber(-8750000).toText())

def Test_Viewers():
    print('Đang test Viewers')
    v = ViewOrders()
    print(v.to_views(symbol='DGC'))

def Test_Notes():
    db = NoteDb()
    note = Note(text='Đây là note thứ 2')
    db.addItem(note)
    print(db.getAll())
    print(db.getItemsOfToday())

def Test_DateData():
    s = Stock(name='KDH')
    d = DateData(symbol=s.name, index=0, df_all_data=s.df_data)
    print(f'MA10: {d.getMA(window=10)}')
    print(f'MA20: {d.getMA(window=20)}')
    print(f'MA50: {d.getMA(window=50)}')
    print(f'MA100: {d.getMA(window=100)}')

    windows = [10,20,50,100, 200, 5*4*12]
    for w in windows:
        print(f'Max price {w}: {d.getMaxPrice(window=w)}')

    windows = [10,20,50,100, 200, 5*4*12]
    for w in windows:
        print(f'Min price {w}: {d.getMinPrice(window=w)}')

    windows = [0,1,2,3,5,10]
    for w in windows:
        print(f'Biến động giá {w}: {d.get_distance_price(window=w)}')

def Test_NextDay_DateData():
    s = Stock(name='VND')
    d = DateData(symbol=s.name, index=10, df_all_data=s.df_data)
    print(f'Candles: {d.getNextCandle(nextDays=3)}')
    print(f'Profit: {d.getProfit(nextDays=3):,.2f} (%)')
    

import pandas as pd

def Test_GetAllStocks():
    stocks = listing_companies()['ticker']
    df = pd.DataFrame(stocks)
    df.to_excel('./stocks.xlsx')
    return stocks.to_list()

def runTest():
    # Test_DateRange()
    # Test_DividendStock()
    #Test_Stock()
    Test_NextDay_DateData()
    # Test_AnalysisPrice()
    # Test_Translator()
    # Test_Alpha()
    
    # Test_VnDate()
    # Test_AnalysisIntradayData()
    # #Test_DailyReport()
    
    # Test_MongoDb()
    # Test_OrderDb()
    # Test_StockNews()
    # Test_StockOwners()
    #Test_TextBuilder()
    # Test_BotAnswerObj(symbol='DHC')
    # Test_BotAnswer()
    # Test_RichNumber()
    # Test_Viewers()
    # Test_Notes()
    #Test_DateData()
    #Test_GetAllStocks()

    pass

runTest()