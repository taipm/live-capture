import datetime
import requests
from bs4 import BeautifulSoup
from TextHelper import *
import pandas as pd
from UrlCrawler import UrlCrawler
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class TuDoanh:
    def __init__(self) -> None:
        self.url = f'https://dstock.vndirect.com.vn/tu-doanh-popup'
        self.url = f'https://plus24.mbs.com.vn/apps/StockBoard/MBS/market-watch.html#chuyen-dong-to-chuc'
        self.crawler = UrlCrawler(url=self.url)
    
    def getData(self):
        html = self.crawler.getHtmlFromUrl(url=self.url)[0]
        html = pd.read_table(html)
        print(html)
        return html

    def getfirst(self):
        #market-box market-forex
        content = self.crawler.getContent(url=self.url,css_class='market-forex__table')
        print(content)
        return content

    def getPdf(self):
        import camelot

        # extract all the tables in the PDF file
        abc = camelot.read_pdf("20221220.pdf") #address of file location

        # print the first table as Pandas DataFrame
        print(abc[0].df)



t = TuDoanh()
#t.getData()
t.getPdf()
