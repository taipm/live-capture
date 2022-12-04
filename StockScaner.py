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
                if stock.liquidity_min >= 5:

                    if stock.TODAY.isBreak52Week():
                        self.dailyMarket.addBreak52Weeks(symbol=symbol)

                    if stock.TODAY.isCE:
                        self.dailyMarket.addCE(symbol=symbol)
                        
                    if stock.TODAY.isFL:
                        self.dailyMarket.addFL(symbol=symbol)

                    if stock.TODAY.isGreen:
                        self.dailyMarket.addGREEN(symbol=symbol)
                        
                    if stock.TODAY.isRED:
                        self.dailyMarket.addRED(symbol=symbol)
                    
                    if stock.TODAY.isHighest:
                        self.dailyMarket.addHighest(symbol=symbol)

                    if stock.TODAY.isLowest:
                        self.dailyMarket.addLowest(symbol=symbol)

                    if stock.TODAY.isSwing:
                        self.dailyMarket.addSwing(symbol=symbol)

                    if stock.TODAY.isSleep:
                        self.dailyMarket.addSleep(symbol=symbol)

                    if stock.TODAY.isThroughMA(window=10):
                        self.dailyMarket.addMA10(symbol=symbol)
                    
                    if stock.TODAY.isThroughMA(window=20):
                        self.dailyMarket.addMA20(symbol=symbol)

                    if stock.TODAY.isThroughMA(window=50):
                        self.dailyMarket.addMA50(symbol=symbol)

                    if stock.TODAY.isThroughMA(window=100):
                        self.dailyMarket.addMA100(symbol=symbol)

                    if stock.TODAY.isThroughMA(window=200):
                        self.dailyMarket.addMA200(symbol=symbol)
                    
                    if stock.TODAY.isThroughMAs(windows=[10,20,50,100,200]):
                        self.dailyMarket.addMultiMAs(symbol=symbol)

                    if stock.TODAY.isElephant(window=20):
                        self.dailyMarket.addElephant(symbol=symbol)

                    if stock.TODAY.isBreakFlat():
                        self.dailyMarket.addBreakFlat(symbol=symbol)
                    
                    if stock.TODAY.isThroughMA(window=10):
                        self.dailyMarket.addBreakFlat(symbol=symbol)

        return self.dailyMarket
    
    def __str__(self) -> str:
        if self.dailyMarket is None:
            self.scan()
        print(f'Scaner: {self.dailyMarket}')
        return self.dailyMarket





    