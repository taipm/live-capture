import requests
from bs4 import BeautifulSoup
import pandas as pd
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class CrawlerCafeF:
    #https://www.includehelp.com/mcq/python-mcqs.aspx
    def __init__(self, url):
        self.url = url

    def get_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_links(self):
        html = self.get_html()
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('http'):
                    links.append(href)
            return links
        else:
            return None

    def get_text(self):
        html = self.get_html()
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            content = soup
            #content = soup.find('div', {'class': 'main-panel'})
            if content is not None:
                return content.get_text().strip()
            else:
                return ''

    def get_tables(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        #def getTables(url):
        tables = pd.read_html(self.url, encoding="UTF8")
        if len(tables) > 0:
            return tables
        else:
            return None

import re
def clean_text(text):
    # Loại bỏ các ký tự không phải chữ cái, số hoặc dấu cách
    #text = re.sub(r'[^\w\s]', ' ', text, flags=re.UNICODE)
    # Chuyển văn bản thành chữ thường
    #text = text.lower()
    # Loại bỏ khoảng trắng thừa và ký tự xuống dòng
    #text = re.sub(r'\s+', ' ', text, flags=re.UNICODE).strip()
    while '\n\n' in text:
        text = text.replace('\n\n','\n')
    return text

url = 'https://s.cafef.vn/du-lieu.chn'
c = CrawlerCafeF(url = url)

items = c.get_tables()
for item in items:
    print(item)



import requests

symbol = "^dji"  # DXY symbol for Stooq API
url = f"https://stooq.com/q/l/?s={symbol}&f=sd2t2ohlcv&h&e=csv"  # Stooq API URL for DXY
print(url)
response = requests.get(url)

# Decode the response content as a string and split it into lines
content = response.content.decode("utf-8")
lines = content.strip().split("\n")

# Get the latest DXY price from the second line of the response
latest_data = lines[1].split(",")
latest_dxy_price = latest_data[6]

# Check if the DXY price is valid before converting it to a float
if latest_dxy_price != "N/D":
    latest_dxy_price = float(latest_dxy_price)
    print("The latest DXY price is:", latest_dxy_price)
else:
    print("Unable to retrieve the latest DXY price")

import investpy

df = investpy.get_stock_historical_data(stock='AAPL',
                                        country='United States',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')
print(df.head())