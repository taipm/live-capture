class DailyReport:
    def __init__(self) -> None:
        self.title = f'{StrTODAY} - [Dấu hiệu] - Big trend UP'
        self.content = self.get_daily_report()

    def get_daily_report(self):
        output = ''
        stocks = db.get_all_stocks_db()
        print(stocks)
        errors = []
        for symbol in stocks:
            try:
                s = SupperStock(name=symbol)
                if (s.has_supper_volume):
                    output += f'{s.summary()}'
            except:
                errors.append(symbol)
        print(errors)
        return output

    def updateBlog(self):
        title = self.title
        content = self.content
        blog = Blog()
        url = blog.post(title=title,content=content,tags='daily report')
        return url
    
    def __str__(self) -> str:
        return f'{self.title}\n{self.content}'

# d = DailyReport()
# print(d)
# d.updateBlog()
# print(d.updateBlog())