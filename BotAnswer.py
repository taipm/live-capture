from FinanceStock import FinanceStock
from IntradayData import AnalysisIntradayData
from Stock import Stock
from BlogManager import *
from vnstock import *
from DateHelper import *
from pathlib import Path
from DayData import *
from TextCommand import BotCommand
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
            print(self.query)
            return RichNumber(self.query).rich_text
        elif(len(self.query)==3):
            s = Stock(name= self.query.upper())
            
            output += s.Describe()
            output += DayData(s.name,index=0,df_all_data= s.df_data,count_days=10).summary
            # analysis_intraday = AnalysisIntradayData(symbol=s.name)
            # output += f'\nIntraday:\n{analysis_intraday.GetSummary()}'
            f = FinanceStock(symbol=s.name)
            output += '\nCổ tức: ' + f.get_avg_dividend()
            output += f'\nhttps://fireant.vn/top-symbols/content/symbols/{s.name}'
            post = BlogPost(title=self.query,content=output,tags=s.name)
            link = post.update_to_blog()
            print(f'LINK: {link}')
            output += f'\nBlog: {link}'
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
    
    def answer_two_numbers(self):
        command = BotCommand(self.query)
        a,b = command.is_two_numbers()
        return percent(a,b)

def Test():
    bot = BotAnswer('HPG, VND, FRT')
    bot.answer_stocks()

#Test()