from BotTranslator import BotTranslator
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
        tran = BotTranslator(query)
        return tran.transText

    def answer(self):
        res = client.query(input=self.text)
        answer = next(res.results).text
        return answer