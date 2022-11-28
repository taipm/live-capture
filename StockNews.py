import datetime
import requests
from bs4 import BeautifulSoup
from TextHelper import *
import pandas as pd
from UrlCrawler import UrlCrawler as crawler
#from urllib.request import Request, urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class News:
    def __init__(self, title, time:str) -> None:
        self.title = title
        self.time = time

    def isShortime(self):
        month = str(datetime.datetime.now().month)
        year = str(datetime.datetime.now().year)

        if (month in self.time) and (year in self.time):
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.title} [{self.time}]'

class StockNewsFromCafeF:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()        
        self.url = f'https://s.cafef.vn/tin-doanh-nghiep/{self.symbol.lower()}/Event.chn'

    def getNews(self)->list[News]:
        lines = crawler.getTextFromUrl(self.url).splitlines()[1:]
        results = []
        for index, line in enumerate(lines):
            if self.symbol in line:
                news = News(title=line,time=lines[index-1])
                results.append(news)
        return results
    def getNewsInMonth(self)->list[News]:
        results = []
        news = self.getNews()
        for item in news:
            if item.isShortime():
                results.append(item)
        return results

    def __str__(self) -> str:
        news = self.getNews()
        return f'CafeF: {self.symbol}\n{len(news)}'


class StockNewsFromBSC:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.url = f'https://www.bsc.com.vn/cong-ty/tong-quan/{self.symbol}'
        self.textContent = self.read_url()
        self.text = self.clean()
        self.lines = self.text.splitlines()
        self.tables = pd.read_html(self.url)

    def read_url(self):
        URL = self.url
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        return toStandard(soup.text)

    def get_stock_info(self):
        return self.tables[0]

    def get_stocks_in_sector(self):
        return self.tables[1][self.tables[1]['Giá'] > 0]

    def to_string(self):
        for line in self.lines:
            print(line)
    
    def clean(self):
        start_get = 'Mã CK'
        end_get = 'Trụ sở chính'
        start_index = self.textContent.index(start_get)
        end_index = self.textContent.index(end_get)
        return self.textContent[start_index:end_index]
    
    def get_news(self):#->list[News]:
        rs = []
        for l in self.lines:
            if self.symbol + ":" in l:
                index = self.lines.index(l)
                text_item = l + ':' + f'{self.lines[index+1]}'
                rs.append(text_item)
        return rs

class StockNews:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()
        self.bsc_news = StockNewsFromBSC(self.symbol)
        self.cafef_news = StockNewsFromCafeF(self.symbol)
    
    def getNews(self)->list[News]:
        news = []
        #news += self.bsc_news.get_news()
        news += self.cafef_news.getNews()
        return news

    def __str__(self) -> str:
        output = ''
        news = self.getNews()
        n = 5
        if len(news) < 5:
            n = len(news)
        for item in news[0:n]:
            output += f'\n{News(title = item.title, time = item.time)}'
        return output