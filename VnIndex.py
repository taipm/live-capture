from UrlHelper import getHtmlFromUrl, getTextFromUrl
import pandas as pd
import html5lib
import lxml
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class VnindexDay:
    def __init__(self, date, close, change,volume, liquidity, volume_agree, liquidity_agree, open, high,low) -> None:
        pass
class VnIndex:
    def __init__(self) -> None:
        self.url_history = 'https://s.cafef.vn/Lich-su-giao-dich-VNINDEX-1.chn#data'
        self.df_data = self.to_df_data()
    
    def get_history_data(self):        
        df_data = pd.read_html(self.url_history)[2].iloc[2:]
        # data_items = []
        # for i in range(0,len(df_data)-1):
        #     data_items.append(VnindexDay())
        #print(df_data.to_markdown())
        return df_data
    
    def to_df_data(self):
        df = self.get_history_data()
        df['date'] = df[0]
        del df[0]
        df['close'] = df[1]
        del df[1]
        df['change'] = df[2]
        del df[2]
        del df[3]
        df['volume'] = df[4]
        del df[4]
        df['liquidity'] = df[5]
        del df[5]
        df['volume_agree'] = df[6]
        del df[6]
        df['liquidity_agree'] = df[7]
        del df[7]
        df['open'] = df[8]
        del df[8]
        df['high'] = df[9]
        del df[9]
        df['low'] = df[10]
        del df[10]

        return df
vni = VnIndex()
print(vni.df_data.to_markdown())

# class StockInfo:
#     def __init__(self, symbol) -> None:
#         self.symbol = symbol.upper()
#         self.url = f'https://www.bsc.com.vn/cong-ty/tong-quan/{self.symbol}'
#         self.textContent = self.read_url()        
#         self.text = self.clean()
#         self.lines = self.text.splitlines()

#     def read_url(self):
#         URL = self.url
#         page = requests.get(URL)
#         soup = BeautifulSoup(page.content, "html.parser")        
#         return to_standard(soup.text)

#     def to_string(self):
#         for line in self.lines:
#             print(line)
    
#     def clean(self):
#         start_get = 'Mã CK'
#         end_get = 'Trụ sở chính'
#         start_index = self.textContent.index(start_get)
#         end_index = self.textContent.index(end_get)
#         return self.textContent[start_index:end_index]