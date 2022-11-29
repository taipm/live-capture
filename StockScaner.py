import db
from Stock import Stock
from DailyMarketScore import DailyMarketScore

class StockScaner:
    def __init__(self) -> None:
        self.symbols = db.get_all_stocks_db()#[0:10]
        self.dailyMarket = DailyMarketScore()

    def scan(self)->DailyMarketScore:
        Errors = ['C99']
        for symbol in self.symbols:
            if symbol not in Errors:
                stock = Stock(name=symbol)
                if stock.liquidity_avg >= 5:
                    if stock.TODAY.isCE:
                        self.dailyMarket.addCE(symbol=symbol)
                        
                    if stock.TODAY.isFL:
                        self.dailyMarket.addFL(symbol=symbol)

                    if stock.TODAY.isGreen:
                        self.dailyMarket.addGREEN(symbol=symbol)
                        
                    if stock.TODAY.isRED:
                        self.dailyMarket.addGREEN(symbol=symbol)
                    
                    if stock.TODAY.isHighest:
                        self.dailyMarket.addHighest(symbol=symbol)

                    if stock.TODAY.isLowest:
                        self.dailyMarket.addLowest(symbol=symbol)

                    if stock.TODAY.isSwing:
                        self.dailyMarket.addSwing(symbol=symbol)

                    if stock.TODAY.isSleep:
                        self.dailyMarket.addSleep(symbol=symbol)

        return self.dailyMarket
    
    def __str__(self) -> str:
        if self.dailyMarket is None:
            self.scan()
        print(f'Scaner: {self.dailyMarket}')
        return self.dailyMarket





    