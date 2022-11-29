from datetime import date
from DailyMarketScore import DailyMarketScore
import db
from SupperStock import SupperStock
from BlogManager import Blog
from VnDate import VnDate
class DailyReport:
    format_date = "%Y-%m-%d"
    def __init__(self) -> None:
        self.date = VnDate(date.today()).today
        self.title = f'{self.date.strftime(self.format_date)} - Dấu hiệu cổ phiếu mạnh nổi bật thị trường'
        self.content = self.get_daily_report()

    def get_daily_report(self):
        output = ''
        symbols = db.get_all_stocks_db()
        print(symbols)
        errors = []
        short_desc = ''
        select_stocks = []
        #symbols = ['ASM', 'SSI','PVT','HAG', 'DGC']
        for symbol in symbols:
            try:
                s = SupperStock(name=symbol)
                if (s.has_supper_volume):
                    select_stocks.append(s.name)
                    short_desc += s.name
                    output += f'{s.summary()}'
            except:
                errors.append(symbol)
        print(errors)

        html_report = f'Danh sách cổ phiếu mạnh : {len(select_stocks)} \n{select_stocks}'
        output = f'{html_report}\n{output}'
        output += f'\nCổ phiếu lỗi: {errors}'
        return output

    def updateBlog(self):
        title = self.title
        content = self.content
        blog = Blog()
        url = blog.post(title=title,content=content,tags='daily report')
        return url

    def run(self):
        self.updateBlog()

    def __str__(self) -> str:
        return f'{self.title}\n{self.content}'