from DateHelper import StrTODAY
from MongoDb import ObjectDb

class DailyMarketScore(ObjectDb):
    def __init__(self) -> None:
        super().__init__()

        self.summary:str

        #DANH SÁCH CÁC CỔ PHIẾU PHÙ HỢP VỚI TIÊU CHÍ (NHƯ TÊN)
        self.CEs = []
        self.FLs = []
        self.Highest = []
        self.Swings = []
        self.Sleeps = []
        self.Lowest = []
        self.Elephants = []
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

    
    def add(self, symbol:str,type:str):
        pass
    
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

    def addElephant(self, symbol:str):
        self.Elephants.append(symbol)
    
    def process(self):
        self.CEs = set(self.CEs)

    def postToBlog(self):
        pass

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

    def Summary(self) -> str:
        output = f'DAILY MARKET SUMMARY: {StrTODAY}'
        output = f'\nĐánh giá trạng thái: {self.StateMarket()}\n'
        output += f'\nCE ({len(self.CEs)}):\n{self.CEs}\n'
        output += f'\nFL ({len(self.FLs)}):\n{self.FLs}\n'
        output += f'\nHighest ({len(self.Highest)}):\n{self.Highest}\n'
        output += f'\nLowest ({len(self.Lowest)}):\n{self.Lowest}\n'
        output += f'\nSwings ({len(self.Swings)}):\n{self.Swings}\n'
        output += f'\nSleep ({len(self.Sleeps)}):\n{self.Sleeps}'
        output += f'\n{"="*40}\n'
        return output
    # def __str__(self) -> str:
    #     output = f'DAILY MARKET SUMMARY: {StrTODAY}'
        
    #     output += f'\nCE ({len(self.CEs)}):\n{self.CEs}'
    #     output += f'\nFL ({len(self.FLs)}):\n{self.FLs}'
    #     output += f'\nHighest ({len(self.Highest)}):\n{self.Highest}'
    #     output += f'\nLowest ({len(self.Lowest)}):\n{self.Lowest}'
    #     output += f'\n{"="*40}\n'

    #     return output