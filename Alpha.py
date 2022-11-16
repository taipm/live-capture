from Config import ALPHA_APP_ID
from wolframalpha import *
from TextHelper import toStandard
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import translate
from langdetect import detect

client = Client(ALPHA_APP_ID)
class Alpha:
    def __init__(self, query) -> None:
        self.query = query
        self.text = self.correctQuery()
        self.answerText = self.answer()
    
    def correctQuery(self):
        query = toStandard(self.query)
        src_lang = detect(query)

        #text = None
        
        if(src_lang != 'en'):
            trans = translate.Translator(to_lang='en')
            transText = trans.translate(query)
            print(transText)
            return transText
            # print(src_lang)
            # print(text)
        else:
            return query
        #return text

    def answer(self):
        res = client.query(input=self.text)
        print(res)
        answer = ''
        #answer = next(res.results).text
        #print(answer)
        return answer

# Includes only text from the response
#answer = next(res.results).text
  
#print(answer)
# a = Alpha(query="How far from earth to moon")
# print(a.answerText)

# a = Alpha(query="Khoảng cách từ trái đất đến mặt trăng")
# print(a.answerText)