from DateHelper import StrTODAY
from MongoDb import ObjectDb
from vnstocklib.StockChart import StockChart

class DailyMarketScore(ObjectDb):
    def __init__(self) -> None:
        super().__init__()

        self.summary:str

        #DANH SÁCH CÁC CỔ PHIẾU PHÙ HỢP VỚI TIÊU CHÍ (NHƯ TÊN)
        self.CEs = []        
        self.FLs = []

        self.Highest = []
        self.Lowest = []

        self.Swings = []
        self.Sleeps = []
        
        self.Elephants = []
        self.BreakFlats = []
        self.Break52Weeks = []

        self.GREENs = []
        self.YELLOWs = []
        self.REDs = []
        self.MaxVols = []
        self.MaxPrice = []
        self.MinVols = []
        self.MinPrice = []
        self.MA50s = [] #>=MA50
        self.MA20s = []
        self.MA10s = []
        self.MA100s = []
        self.MA200s = []
        self.MultiMAs = []

        self.VolumeUps = [] #Volume tăng liên tục
        self.VolumeDowns = [] #Volume giảm liên tục

        self.RecommendList = [] #Danh sách khuyến nghị

        #GAPS
        self.GapUps = []
        self.GapDowns = []
        
        #MÔ HÌNH THEO MẪU LÝ THUYẾT
        self.DarvasList = []
        self.SepaList = []
        self.CanslimList = []

        #THỊ TRƯỜNG CHUNG
        self.MarketIndex:float #Là điểm số thị trường
        self.MarketLiquidity:float
        self.MarketColor:str

    
    def addBreak52Weeks(self, symbol:str):
        self.Break52Weeks.append(symbol)
    
    def addElephant(self, symbol:str):
        self.Elephants.append(symbol)

    def addBreakFlat(self, symbol:str):
        self.BreakFlats.append(symbol)

    def addMA10(self, symbol:str):
        self.MA10s.append(symbol)
    
    def addMA20(self, symbol:str):
        self.MA20s.append(symbol)

    def addMA50(self, symbol:str):
        self.MA50s.append(symbol)
    
    def addMA100(self, symbol:str):
        self.MA100s.append(symbol)

    def addMA200(self, symbol:str):
        self.MA200s.append(symbol)

    def addMultiMAs(self, symbol:str):
        self.MultiMAs.append(symbol)

    def addSwing(self, symbol:str):
        self.Swings.append(symbol)
    
    def addSleep(self, symbol:str):
        self.Sleeps.append(symbol)

    def addHighest(self, symbol:str):
        self.Highest.append(symbol)

    def addLowest(self, symbol:str):
        self.Lowest.append(symbol)

    def addCE(self, symbol:str):
        self.CEs.append(symbol)

    def addFL(self, symbol:str):
        self.FLs.append(symbol)
    
    def addGREEN(self, symbol:str):
        self.GREENs.append(symbol)
    
    def addYELLOW(self, symbol:str):
        self.YELLOWs.append(symbol)
    
    def addRED(self, symbol:str):
        self.REDs.append(symbol)    
    
    @property
    def recommends(self):
        symbols = ''
        symbols += ','.join(self.Elephants) + ','
        symbols += ','.join(self.BreakFlats) + ','
        symbols += ','.join(self.Break52Weeks) + ','
        symbols += ','.join(self.MultiMAs)
        print(symbols)
        symbols = symbols.split(',')[1:]
        print(symbols)
        return list(set(symbols))

    def saveToDb(self):
        pass

    def StateMarket(self):
        count_CEs = len(self.CEs)
        count_FLs = len(self.FLs)
        rate = 100
        stateText = ''
        if count_FLs != 0:
            rate = count_CEs/count_FLs
        if rate == 100:
            stateText = 'Đang tăng rất mạnh'
        elif rate >= 2:
            stateText = 'Đang tăng'
        else:
            stateText = 'Đang yếu. Cẩn trọng. Hạn chế giao dịch'
        
        return f'Điểm: {rate} - ' + stateText

    def exportToBlog(self):
        symbols = self.recommends
        html = ''
        for symbol in symbols:
            stock = StockChart(symbol=symbol)
            htmlStock = f'\n{symbol} - {StrTODAY}'
            htmlStock += f'\n{stock.dailyChartUrl}\n{stock.weeklyChartUrl}'
            html += f'\n{htmlStock}'
        return html

    def Summary(self) -> str:
        output = f'DAILY MARKET SUMMARY: {StrTODAY}'
        output = f'\nĐánh giá trạng thái: {self.StateMarket()}\n'
        
        output += f'\nElephants ({len(self.Elephants)}):\n{self.Elephants}\n'
        output += f'\nVượt đỉnh 52 tuần : ({len(self.Break52Weeks)}):\n{self.Break52Weeks}\n'
        output += f'\nVượt nền phẳng (flat): ({len(self.BreakFlats)}):\n{self.BreakFlats}\n'

        output += f'\nMA10 ({len(self.MA10s)}):\n{self.MA10s}\n'
        output += f'\nMA20 ({len(self.MA20s)}):\n{self.MA20s}\n'
        output += f'\nMA50 ({len(self.MA50s)}):\n{self.MA50s}\n'
        output += f'\nMA100 ({len(self.MA100s)}):\n{self.MA100s}\n'
        output += f'\nMA200 ({len(self.MA200s)}):\n{self.MA200s}\n'
        output += f'\nMA-GIAO NHAU: ({len(self.MultiMAs)}):\n{self.MultiMAs}\n'

        output += f'\nCE ({len(self.CEs)}):\n{self.CEs}\n'
        output += f'\nFL ({len(self.FLs)}):\n{self.FLs}\n'
        output += f'\nHighest ({len(self.Highest)}):\n{self.Highest}\n'
        output += f'\nLowest ({len(self.Lowest)}):\n{self.Lowest}\n'
        output += f'\nSwings ({len(self.Swings)}):\n{self.Swings}\n'
        output += f'\nSleep ({len(self.Sleeps)}):\n{self.Sleeps}'
        output += f'\n{"="*40}\n'
        output += f'\nLỰA CHỌN QUAN SÁT: \n ({len(self.recommends)}):\n{self.recommends}'
        output += f'\n{self.exportToBlog()}'

        return output