import datetime
from DateHelper import StrTODAY
from MongoDb import ObjectDb
from RecommendDb import RecommendDb
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
        self.Covers = []
        self.Sleeps = []
        
        self.Elephants = []
        self.UpVolumes = []
        self.MinVolumes = []
        self.BreakFlats = []
        self.Break52Weeks = []

        self.GREENs = []
        self.YELLOWs = []
        self.REDs = []
        self.MaxVols = []
        self.MaxPrice = []
        self.MinVols = []
        self.MinPrice = []

        self.ThroughMA50s = []
        self.ThroughMA20s = []
        self.ThroughMA10s = []
        self.ThroughMA100s = []
        self.ThroughMA200s = []
        self.ThroughMultiMAs = []

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

    def addUpVolume(self, symbol:str):
        self.UpVolumes.append(symbol)

    def addMinVolume(self, symbol:str):
        self.MinVolumes.append(symbol)

    def addCover(self, symbol:str):
        self.Covers.append(symbol)

    def addBreak52Weeks(self, symbol:str):
        self.Break52Weeks.append(symbol)
    
    def addElephant(self, symbol:str):
        self.Elephants.append(symbol)

    def addBreakFlat(self, symbol:str):
        self.BreakFlats.append(symbol)

    def addMA10(self, symbol:str):
        self.ThroughMA10s.append(symbol)
    
    def addMA20(self, symbol:str):
        self.ThroughMA20s.append(symbol)

    def addMA50(self, symbol:str):
        self.ThroughMA50s.append(symbol)
    
    def addMA100(self, symbol:str):
        self.ThroughMA100s.append(symbol)

    def addMA200(self, symbol:str):
        self.ThroughMA200s.append(symbol)

    def addMultiMAs(self, symbol:str):
        self.ThroughMultiMAs.append(symbol)

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
        symbols += ','.join(self.Covers) + ','
        symbols += ','.join(self.UpVolumes) + ','
        symbols += ','.join(self.MinVolumes) + ','
        symbols += ','.join(self.ThroughMultiMAs)
        print(symbols)
        symbols = set(symbols.split(','))
        print(symbols)
        return list(symbols)

    def saveToDb(self):
        _now = str(datetime.datetime.now())
        print(_now)
        is_deleted_today = False
        if len(self.MinVolumes) > 0:
            db = RecommendDb(recommendLst=self.MinVolumes, type_recommend='MinVolumes', date_recommend=_now)
            if not is_deleted_today:
                db.deleteItemsOfToday()
                is_deleted_today = True
            db.saveAll()
        if len(self.Elephants) > 0:
            db = RecommendDb(recommendLst=self.Elephants, type_recommend='Elephants', date_recommend=_now)
            if not is_deleted_today:
                db.deleteItemsOfToday()
                is_deleted_today = True
            db.saveAll()
        if len(self.BreakFlats) > 0:
            db = RecommendDb(recommendLst=self.BreakFlats, type_recommend='BreakFlats', date_recommend=_now)
            if not is_deleted_today:
                db.deleteItemsOfToday()
                is_deleted_today = True
            db.saveAll()
        if len(self.ThroughMultiMAs) > 0:
            db = RecommendDb(recommendLst=self.ThroughMultiMAs, type_recommend='ThroughMultiMAs', date_recommend=_now)
            if not is_deleted_today:
                db.deleteItemsOfToday()
                is_deleted_today = True
            db.saveAll()
        if len(self.Break52Weeks) > 0:
            db = RecommendDb(recommendLst=self.Break52Weeks, type_recommend='Break52Weeks', date_recommend=_now)
            if not is_deleted_today:
                db.deleteItemsOfToday()
                is_deleted_today = True
            db.saveAll()
        if len(self.Covers) > 0:
            db = RecommendDb(recommendLst=self.Covers, type_recommend='Covers', date_recommend=_now)
            if not is_deleted_today:
                db.deleteItemsOfToday()
                is_deleted_today = True
            db.saveAll()
        if len(self.UpVolumes) > 0:
            db = RecommendDb(recommendLst=self.Covers, type_recommend='CoverVolumes', date_recommend=_now)
            if not is_deleted_today:
                db.deleteItemsOfToday()
                is_deleted_today = True
            db.saveAll()


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
        output += f'\nCovers ({len(self.Covers)}):\n{self.Covers}\n'
        output += f'\nUpVolumes ({len(self.UpVolumes)}):\n{self.UpVolumes}\n'
        output += f'\nMin-Volumes ({len(self.MinVolumes)}):\n{self.MinVolumes}\n'
        output += f'\nVượt đỉnh 52 tuần : ({len(self.Break52Weeks)}):\n{self.Break52Weeks}\n'
        output += f'\nVượt nền phẳng (flat): ({len(self.BreakFlats)}):\n{self.BreakFlats}\n'

        output += f'\nMA10 ({len(self.ThroughMA10s)}):\n{self.ThroughMA10s}\n'
        output += f'\nMA20 ({len(self.ThroughMA20s)}):\n{self.ThroughMA20s}\n'
        output += f'\nMA50 ({len(self.ThroughMA50s)}):\n{self.ThroughMA50s}\n'
        output += f'\nMA100 ({len(self.ThroughMA100s)}):\n{self.ThroughMA100s}\n'
        output += f'\nMA200 ({len(self.ThroughMA200s)}):\n{self.ThroughMA200s}\n'
        output += f'\nMA-GIAO NHAU: ({len(self.ThroughMultiMAs)}):\n{self.ThroughMultiMAs}\n'

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