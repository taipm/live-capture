import requests
from bs4 import BeautifulSoup
from TextHelper import *
import pandas as pd
import html5lib
from urllib.request import Request, urlopen
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class StockInfo:
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
    
    def get_news(self):
        rs = []
        for l in self.lines:
            if self.symbol + ":" in l:
                index = self.lines.index(l)
                text_item = l + ':' + f'{self.lines[index+1]}'
                rs.append(text_item)
                print(text_item)
        return rs


