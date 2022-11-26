
from datetime import date
from Alpha import Alpha
from AnalysisList import AnalysisList
from AnalysisPrices import AnalysisPrice
from BotAnswer import BotAnswer
from BotTranslator import BotTranslator
from DailyReport import DailyReport
from DateRange import DateRange
from FinanceStock import FinanceStock
from IntradayData import AnalysisIntradayData
from MongoDb import MongoDb
from Notes import Note, NoteDb
from OrderDb import OrderDb
from RichNumber import RichNumber
from Stock import Stock
from vnstocklib.StockInfo import StockInfo
from TextBuilder import TextBuilder
from Viewers import ViewOrders
from VnDate import VnDate

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
    print(b.text_markdown)
    b.to_string()

def Test_StockInfo():
    s = StockInfo("DIG")
    print(s.text)
    print(s.get_stock_info().to_markdown())
    print(s.get_stocks_in_sector().to_markdown())
    print(s.get_news())

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
    db.addItem(note.to_json())
    print(db.getAll())
    print(db.getItemsOfToday())
    
def runTest():
    # Test_DateRange()
    # Test_FinanceStock()
    # Test_Stock()
    # Test_AnalysisPrice()
    # Test_Translator()
    Test_Alpha()
    
    # Test_VnDate()
    # Test_AnalysisIntradayData()
    #Test_DailyReport()
    
    # Test_MongoDb()
    # Test_OrderDb()
    # Test_StockInfo()
    # Test_TextBuilder()
    # Test_BotAnswerObj(symbol='DHC')
    # Test_BotAnswer()
    # Test_RichNumber()
    # Test_Viewers()
    Test_Notes()

runTest()