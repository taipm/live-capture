
from UrlCrawler import UrlCrawler
import pandas as pd

class StockNews:
    def __init__(self, symbol) -> None:
        self.symbol = symbol.upper()        
        self.url = f'https://s.cafef.vn/tin-doanh-nghiep/{self.symbol.lower()}/Event.chn'

    def getNews(self):
        text = UrlCrawler.getTextFromUrl(self.url)
        return text

# s = StockNews(symbol='HAX')
# print(s.getText())
#print(s.getNewsFromCafeF())
