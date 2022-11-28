
import requests
from bs4 import BeautifulSoup
from TextHelper import *
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class UrlCrawler:
    def __init__(self, url) -> None:
        self.url = url
    
    @staticmethod
    def getTextFromUrl(url):
        page = requests.get(url=url)
        soup = BeautifulSoup(page.content, "html.parser")        
        return toStandard(soup.text)

    @staticmethod
    def getHtmlFromUrl(url):
        page = requests.get(url=url)    
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.contents
        
    @staticmethod
    def getTables(url):
        tables = pd.read_html(url, encoding="UTF8")
        if len(tables) > 0:
            return tables
        else:
            return None


# url ='https://www.channelnewsasia.com/business/vietnam-property-developer-no-va-land-cash-crunch-3049806'
# txt = getTextFromUrl(url)

# from BotTranslator import BotTranslator

# translator = BotTranslator(txt)
# print(translator.transText)