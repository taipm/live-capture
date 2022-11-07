from UrlHelper import getTextFromUrl


class VnIndex:
    def __init__(self) -> None:
        self.url_history = 'https://s.cafef.vn/Lich-su-giao-dich-VNINDEX-1.chn#data'
    
    def get_history_data(self):
        return getTextFromUrl(self.url_history)


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