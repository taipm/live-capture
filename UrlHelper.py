
import requests
from bs4 import BeautifulSoup
from TextHelper import *

def getTextFromUrl(url):    
    page = requests.get(url=url)
    soup = BeautifulSoup(page.content, "html.parser")        
    return to_standard(soup.text)

def getHtmlFromUrl(url):
    page = requests.get(url=url)    
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.contents


# url ='https://www.channelnewsasia.com/business/vietnam-property-developer-no-va-land-cash-crunch-3049806'
# txt = getTextFromUrl(url)

# from BotTranslator import BotTranslator

# translator = BotTranslator(txt)
# print(translator.transText)