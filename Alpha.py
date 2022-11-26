from BotTranslator import BotTranslator
from Config import ALPHA_APP_ID
from wolframalpha import *
from Notes import Note, NoteDb
from TextHelper import toStandard
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
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
        if src_lang == 'vi':
            tran = BotTranslator(query)
            return tran.transText
        else:
            return query

    def answer(self):
        res = client.query(input=self.text)
        answer = next(res.results).text
        return answer

    def addToNotes(self):
        note = Note(text = f'{input} : {self.answerText}')
        db = NoteDb()
        db.addItem(note.to_json())