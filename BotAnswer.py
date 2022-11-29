from DividendStock import DividendStock
from RichNumber import RichNumber
from Stock import Stock
from BlogManager import *
from DateHelper import *
from DayData import *
from Buyers import *
from Viewers import ViewOrders
from vnstock import *

class BotMessage(ObjectDb):
    def __init__(self, question, answer) -> None:
        super().__init__()
        self.question = question
        self.answer = answer
    
    def __str__(self) -> str:
        return f'{self.question} : {self.time}\n{self.answer}'
    
class BotAnswer:
    def __init__(self, query) -> None:
        self.query = query
        self.posts = []
    
    def is_number(self):
        print(self.query)
        if(self.query.isnumeric()):
            print('Là số')
            return True
        else:
            print('Là chữ')
            return False

    def answer(self):
        output = ''
        print(self.query)
        if(self.is_number()):            
            return RichNumber(self.query).rich_text
        elif(len(self.query)==3):
            print(f'Đang xử lý mã : {self.query}')
            s = Stock(name= self.query)
            output += s.summary()            
            output += f'\nhttps://fireant.vn/top-symbols/content/symbols/{s.name}'
            post = BlogPost(title=self.query,content=output,tags=s.name)
            link = post.update_to_blog()
            output += f'\nBlog: {link}'
            
            return f'{output}'
        elif(len(self.query)==4):
            v = ViewOrders()
            return v.to_views(symbol=self.query[1:].upper())

    def answer_stocks(self, stocks):        
        print(f'Đang tìm kết quả: {stocks}')
        lst = []
        for stock in stocks:
            lst.append(stock.strip().upper())
        stocks = ','.join(lst)
        if(len(stocks)>1):            
            print(stocks)
            board = price_board(stocks)
            print(board)
            rs = board.transpose()
            return rs

    # def answer_two_numbers(self):
    #     command = BotCommand(self.query)
    #     a,b = command.is_two_numbers()
    #     return percent(a,b)



#print(TestStock(symbol='VND'))
