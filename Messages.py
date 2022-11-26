from Alpha import Alpha
from MongoDb import ObjectDb
from TextHelper import toStandard
from Viewers import ViewOrders
import db

class Message(ObjectDb):
    def __init__(self, input_text:str) -> None:
        super().__init__()
        self.input = input_text
        self.message = toStandard(input_text)
        self.length = len(self.message)

    def __str__(self) -> str:
        return f'Input: {self.input}\nMessage: {self.message}\nTime: {self.time}'

class AlphaMessage(Message):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        print(f'HistoryOrderMessage: {input_text}')
        self.symbol = None
        self.isValid = False
        self.process()        

    def process(self):
        if self.message.startswith('?'):
            self.message = self.message[1:]
            self.isValid = True
        
        if self.isValid:
            alpha = Alpha(self.message)
            return alpha.answerText
            
    def __str__(self) -> str:
        if(self.symbol is None):
            return f'{self.input} is not valid command for Wolframe Alpha Message'
        return f'Input: {input} -> Wolframe Alpha query: {self.message} : {self.time}'

class TranslateMessage:
    pass

class HistoryOrderMessage(Message):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        print(f'HistoryOrderMessage: {input_text}')
        self.symbol = None        
        self.isValid = False
        self.process()

    def process(self):
        if self.message.startswith('!'):
            if self.length == 4:                             
                stock = self.message[1:].upper()
                stocks = db.get_all_stocks_db()
                if(stock in stocks):
                    self.symbol = stock
                    self.isValid = True

                if self.isValid:
                    stock = self.message[1:].upper()
                    v = ViewOrders()
                    return v.to_views(symbol=self.symbol)
                else:
                    return f'HistoryOrderMessage:'+\
                        f'\nBạn chưa có giao dịch cho mã {self.symbol}'
    
    def __str__(self) -> str:
        if(self.symbol is None):
            return f'{self.input} is not valid command for HistoryOrderMessage'
        return f'Input: {input} -> Stock symbol: {self.symbol} : {self.time}'

# h = HistoryOrderMessage('!VND')
# print(h)

class StockMessage:
    pass

class HandleMessage:
    def __init__(self, input:str) -> None:
        self.command = self.detect()
    
    def detect(self):
        h = HistoryOrderMessage(input_text=input)
        if h.isValid: 
            return h
        return None