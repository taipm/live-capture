import xlsxwriter
import pandas as pd

class ExcelDb:
    def __init__(self, db_file) -> None:
        self.db_file = db_file

    def addRow(self, dataItem):
        workbook = xlsxwriter.Workbook(self.db_file)
        worksheet = workbook.add_worksheet()
        worksheet.write([dataItem])
        workbook.close()

    def print_data(self):
        data = pd.read_excel(self.db_file,engine='openpyxl')
        print(data)


db_file='./data/TradingBook.xlsx'
db = ExcelDb(db_file=db_file)
db.addRow(['VND',100,10])
db.print_data()