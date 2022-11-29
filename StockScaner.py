import db
from Stock import Stock
from DailyMarketScore import DailyMarketScore

class StockScaner:
    def __init__(self) -> None:
        self.symbols = db.get_all_stocks_db()
        self.symbols = ['ASM','DGC','PDR']
        self.dailyMarket = DailyMarketScore()

    def scan(self)->DailyMarketScore:
        for symbol in self.symbols:
            stock = Stock(name=symbol)

            if stock.TODAY.isCE:
                self.dailyMarket.addCE(symbol=symbol)
            
            if stock.TODAY.isFL:
                self.dailyMarket.addFL(symbol=symbol)

            if stock.TODAY.isGreen:
                self.dailyMarket.addGREEN(symbol=symbol)
            
            if stock.TODAY.isRED:
                self.dailyMarket.addGREEN(symbol=symbol)

        return self.dailyMarket
    
    def __str__(self) -> str:
        if self.dailyMarket is None:
            self.scan()
        return self.dailyMarket


scaner = StockScaner()
dailyMarket = scaner.scan()
print(dailyMarket)


    