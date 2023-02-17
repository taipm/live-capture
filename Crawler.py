import requests
from bs4 import BeautifulSoup

class Crawler:
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
            content = soup.find('div', {'class': 'main-panel'})
            if content is not None:
                return content.get_text().strip()
            else:
                return ''
        #     return soup.get_text()
        # else:
        #     return None

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

urls = ["https://www.includehelp.com/data-analytics/mcq.aspx",'https://www.includehelp.com/mcq/python-mcqs.aspx']
texts=[]
for url in urls:
    print(url)
    crawler = Crawler(url)
    links = crawler.get_links()
    text = crawler.get_text()
    texts.append(clean_text(text))

text = texts[0]

# def find_common_sections(text1, text2):
#     # Tách văn bản thành các câu
#     sentences1 = text1.split(". ")
#     sentences2 = text2.split(". ")
    
#     # Tìm đoạn giống nhau giữa 2 văn bản bằng thuật toán LCS
#     m = len(sentences1)
#     n = len(sentences2)
#     lcs = [[0] * (n+1) for i in range(m+1)]
#     for i in range(1, m+1):
#         for j in range(1, n+1):
#             if sentences1[i-1] == sentences2[j-1]:
#                 lcs[i][j] = lcs[i-1][j-1] + 1
#             else:
#                 lcs[i][j] = max(lcs[i][j-1], lcs[i-1][j])
    
#     # Truy vết đoạn trùng nhau bằng cách duyệt lại ma trận LCS
#     common_sections = []
#     i = m
#     j = n
#     while i > 0 and j > 0:
#         if sentences1[i-1] == sentences2[j-1]:
#             common_sections.append(sentences1[i-1])
#             i -= 1
#             j -= 1
#         elif lcs[i-1][j] > lcs[i][j-1]:
#             i -= 1
#         else:
#             j -= 1
    
#     # Đảo ngược kết quả để đưa ra đoạn trùng nhau theo thứ tự xuất hiện trong văn bản
#     common_sections.reverse()
    
#     return common_sections


# commonText = find_common_sections(text1=texts[0],text2=texts[1])
# _text = texts[0]
# #print(commonText)
# for c in commonText:
#     _text = _text.replace(c,'')

#print(text[0:1000])


def extract_text_between(text, start_text, end_text):
    start_index = text.find(start_text)
    if start_index == -1:
        return ''
    
    end_index = text.find(end_text, start_index + len(start_text))
    if end_index == -1:
        return ''
    
    return text[start_index + len(start_text):end_index]

text = extract_text_between(text= text,start_text='(MCQs)', end_text='What\'s New (MCQs)')
print(text[:len(text)-1000])