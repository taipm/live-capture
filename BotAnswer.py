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
        if(len(self.query)==3):
            s = Stock(name= self.query.upper())
            s.Prepare()
            post = BlogPost(title=self.query,content=s.Describe(),tags=s.name)
            post.update_to_blog()
            return f'{s.Describe()}'
            # update.message.reply_text(f'{s.Describe()}')
            # # financeStock = FinanceStock(input_text)
            # # basicInfo = financeStock.getBasicInfo().to_markdown()
            # update.message.reply_text(f'{s.GetTCB()}')
    
