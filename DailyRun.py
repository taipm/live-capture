from BlogManager import Blog
from DailyReport import DailyReport
from DateHelper import StrTODAY
from StockScaner import StockScaner

def runDailyReport():
    d = DailyReport()
    d.run()
    
def dailyScaner():
    scaner = StockScaner()
    dailyMarket = scaner.scan()
    print(dailyMarket)

    title = f'{StrTODAY} - DẤU ẤN THỊ TRƯỜNG'
    content = dailyMarket
    print(f'Run: {title}\n{content}')
    blog = Blog()
    url = blog.post(title=title,content=content.Summary(),tags=f'VnIndex, {StrTODAY}, daily, marketScaner')
    print(url)
    return url

def run():
    #runDailyReport()
    dailyScaner()

run()