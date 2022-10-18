from FinanceStock import FinanceStock
from stock import Stock
from BlogManager import Blog

class QueryHandle:
    pass

class BlogPost:
    def __init__(self, title, content, tags) -> None:
        self.title = title
        self.content = content
        self.tags = tags

    def update_to_blog(self):
        blog = Blog()
        blog.post(title=self.title,content=self.content, tags= self.tags)

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
    
