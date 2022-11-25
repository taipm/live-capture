from datetime import date
from DateHelper import StrTODAY
import db
from SupperStock import SupperStock
from BlogManager import Blog
from VnDate import VnDate
# from htmldocx import HtmlToDocx
# from docx import Document
class DailyReport:
    def __init__(self) -> None:
        self.date = VnDate(date.today()).today
        self.title = f'{StrTODAY} - Dấu hiệu cổ phiếu mạnh nổi bật thị trường'
        self.content = self.get_daily_report()

    def get_daily_report(self):
        output = ''
        stocks = db.get_all_stocks_db()
        print(stocks)
        errors = []
        stocks = ['DGC','ASM']
        for symbol in stocks:
            try:
                s = SupperStock(name=symbol)
                if (s.has_supper_volume):
                    #output += "<hr>"
                    output += f'{s.summary()}'
                    #output += "<br/>"
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
    
    # def exportTo_docx(self):
    #     document = Document()
    #     new_parser = HtmlToDocx()
    #         # do stuff to document
    #     html = self.content
    #     new_parser.add_html_to_document(html, document)

    #         # do more stuff to document
    #     document.save('dailyreport.docx')

    def __str__(self) -> str:
        return f'{self.title}\n{self.content}'