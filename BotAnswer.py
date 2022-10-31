from FinanceStock import FinanceStock
from Stock import Stock
from BlogManager import *
from vnstock import *
from DateHelper import *
from pathlib import Path

class BotAnswer:
    def __init__(self, query) -> None:
        self.query = query
        self.posts = []

    def answer(self):
        output = ''
        if(len(self.query)==3):
            s = Stock(name= self.query.upper())
            s.Prepare()
            post = BlogPost(title=self.query,content=s.Describe(),tags=s.name)
            post.update_to_blog()
            
            output += s.Describe()
            output += '\nCổ tức: ' + FinanceStock(symbol=self.query.upper()).get_avg_dividend()

            return f'{output}'

    def answer_stocks(self):
        stocks = self.query.split(',')
        lst = []
        for stock in stocks:
            lst.append(stock.strip().upper())
        stocks = ','.join(lst)
        if(len(stocks)>1):
            print('Đang query nhiều cổ phiếu')
            print(stocks)
            board = price_board(stocks)
            rs = board.transpose()
            file_path = './data/' + 'your-file-' + 'Intraday-' +str(datetime.now()) + ".xlsx"
            rs.to_excel(file_path)
            print(rs)
            blog = Blog()
            file_url = blog.upload(file_path=file_path)
            print(file_url)
            return file_url
            #return file_path


    def answer_with_chart(self):
        if(len(self.query)==3):
            print('Đang vẽ đồ thị')
            s = Stock(name = self.query.upper())
            s.Prepare()
            file_path = s.draw()
            return file_path
            # update.message.reply_text(f'{s.Describe()}')
            # # financeStock = FinanceStock(input_text)
            # # basicInfo = financeStock.getBasicInfo().to_markdown()
            # update.message.reply_text(f'{s.GetTCB()}')
    
def Test():
    bot = BotAnswer('HPG, VND, FRT')
    bot.answer_stocks()

#Test()